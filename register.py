"""
pbkdf2==1.3
pyaes==1.6.1
requests==2.28.1
"""

import pyaes
from pbkdf2 import PBKDF2
import requests
import secrets
from urllib.parse import unquote, urlparse, parse_qs
import base64
import hashlib
import hmac
import gzip
import json

APP_NAME = "com.amazon.rabbit"
APP_VERSION = "303338310"
DEVICE_NAME = "Le X522"
MANUFACTURER = "LeMobile"
OS_VERSION = "LeEco/Le2_NA/le_s2_na:6.0.1/IFXNAOP5801910272S/61:user/release-keys"


def register_account(maplanding_url):
    parsed_query = parse_qs(urlparse(maplanding_url).query)
    reg_access_token = unquote(parsed_query['openid.oa2.access_token'][0])
    amz_account_id = unquote(parsed_query['openid.identity'][0]).replace(
        'https://www.amazon.com/ap/id/', '')
    #print(reg_access_token)
    #print(amz_account_id)
    device_id = secrets.token_hex(16)
    amazon_reg_data = {
        "auth_data": {
            "access_token": reg_access_token
        },
        "cookies": {
            "domain": ".amazon.com",
            "website_cookies": []
        },
        "device_metadata": {
            "android_id": "52aee8aecab31ee3",
            "device_os_family": "android",
            "device_serial": device_id,
            "device_type": "A1MPSLFC7L5AFK",
            "mac_address": secrets.token_hex(64).upper(),
            "manufacturer": MANUFACTURER,
            "model": DEVICE_NAME,
            "os_version": "30",
            "product": DEVICE_NAME
        },
        "registration_data": {
            "app_name": APP_NAME,
            "app_version": APP_VERSION,
            "device_model": DEVICE_NAME,
            "device_serial": device_id,
            "device_type": "A1MPSLFC7L5AFK",
            "domain": "Device",
            "os_version": OS_VERSION,
            "software_version": "130050002"
        },
        "requested_extensions": [
            "device_info",
            "customer_info"
        ],
        "requested_token_type": [
            "bearer",
            "mac_dms",
            "store_authentication_cookie",
            "website_cookies"
        ],
        "user_context_map": {
            "frc": generate_frc(device_id)
        }
    }

    url = 'https://api.amazon.com/auth/register'
    reg_headers = {"Content-Type": "application/json",
                   "Accept-Charset": "utf-8",
                   "x-amzn-identity-auth-domain": "api.amazon.com",
                   "Connection": "keep-alive",
                   "Accept": "*/*",
                   "Accept-Language": "en-US"
                   }
    res = requests.post(url, json=amazon_reg_data, headers=reg_headers, verify=True)
    if res.status_code != 200:
        print("login failed")
        return({"result": "failure"})

    res = res.json()
    #print(res)
    tokens = res['response']['success']['tokens']['bearer']
    x_amz_access_token = tokens['access_token']
    refresh_token = tokens['refresh_token']
    data = {
        "result":"success",
        "access_token": x_amz_access_token,
        "refresh_token": refresh_token,
        "amz_account_id": amz_account_id
        }
    #print(data)
    with open('userdata/register_data', 'w') as d:
        print(reg_access_token, '\n', amz_account_id, '\n', data, '\n', res, file=d)
    return(data["refresh_token"])

def generate_frc(device_id):
    cookies = json.dumps({
        "ApplicationName": APP_NAME,
        "ApplicationVersion": APP_VERSION,
        "DeviceLanguage": "en",
        "DeviceName": DEVICE_NAME,
        "DeviceOSVersion": OS_VERSION,
        "IpAddress": requests.get('https://api.ipify.org').text,
        "ScreenHeightPixels": "1920",
        "ScreenWidthPixels": "1280",
        "TimeZone": "00:00",
    })
    compressed = gzip.compress(cookies.encode())
    key = PBKDF2(device_id, b"AES/CBC/PKCS7Padding").read(32)
    iv = secrets.token_bytes(16)
    encrypter = pyaes.Encrypter(pyaes.AESModeOfOperationCBC(key, iv=iv))
    ciphertext = encrypter.feed(compressed)
    ciphertext += encrypter.feed()
    hmac_ = hmac.new(PBKDF2(device_id, b"HmacSHA256").read(32), iv + ciphertext, hashlib.sha256).digest()
    return base64.b64encode(b"\0" + hmac_[:8] + iv + ciphertext).decode()

def get_flex_auth_token(refresh_token):
    url = 'https://api.amazon.com/auth/token'
    data = {
        "app_name": APP_NAME,
        "app_version": APP_VERSION,
        "source_token_type": "refresh_token",
        "source_token": refresh_token,
        "requested_token_type": "access_token",
    }
    headers = {
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 10; Pixel 2 Build/OPM1.171019.021)",
        "x-amzn-identity-auth-domain": "api.amazon.com",
    }
    res = requests.post(url, json=data, headers=headers).json()
    #print(res)
    x_amz_access_token = res['access_token']
    #print(x_amz_access_token)
    return(x_amz_access_token)


def refresh(refresh_token):
        with open("userdata/access_token", "w") as t:
                print(get_flex_auth_token(refresh_token), end='', file=t)