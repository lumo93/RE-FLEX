from typing import Tuple
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.backends import default_backend
import base64, requests, time
from cryptography.hazmat.primitives import serialization
import authCycle
import header_data


def create_attestation_key() -> Tuple[ec.EllipticCurvePrivateKey, ec.EllipticCurvePublicKey]:
    private_key = ec.generate_private_key(ec.SECP256R1(), default_backend())
    public_key = private_key.public_key()
    return private_key, public_key

def serialize_and_encode_keys(private_key: ec.EllipticCurvePrivateKey, public_key: ec.EllipticCurvePublicKey) -> Tuple[str, str]:
    serialized_private_key = serialize_private_key(private_key)
    serialized_public_key = serialize_public_key(public_key)
    b64_encoded_private_key = encode_key(serialized_private_key)
    b64_encoded_public_key = encode_key(serialized_public_key)
    return b64_encoded_private_key, b64_encoded_public_key

def serialize_public_key(public_key: ec.EllipticCurvePublicKey) -> bytes:
    return public_key.public_bytes(encoding=serialization.Encoding.DER, format=serialization.PublicFormat.SubjectPublicKeyInfo)
  
def serialize_private_key(private_key: ec.EllipticCurvePrivateKey) -> bytes:
    return private_key.private_bytes(
      encoding=serialization.Encoding.DER,
      format=serialization.PrivateFormat.PKCS8,
      encryption_algorithm=serialization.NoEncryption()
    )
  
def encode_key(serialized_key: bytes) -> str:
    return base64.b64encode(serialized_key).decode()

def load_attestation_private_key(private_key: str) -> ec.EllipticCurvePrivateKey:
    decoded_private_key = base64.b64decode(private_key)
    loaded_private_key = serialization.load_der_private_key(decoded_private_key, password=None, backend=default_backend())
    return loaded_private_key

def attestation_header_refresh(headers: dict):
    headers['X-Amzn-RequestId'] = authCycle.requestIdSelfSingleUse()
    headers['X-Flex-Client-Time'] = str(round(time.time() * 1000))

def register_attestation():
    import userdata.device_tokens as device_tokens
    from key_id import key_id
    headers = header_data.headers.copy()
    attestation_header_refresh(headers)
    headers['X-Amzn-Identity-Auth-Domain'] = '.amazon.com'
    data = {
        "deviceId": device_tokens.deviceId,
        "keyAttestation": [],
        "publicKey": device_tokens.publicAttestationKey
    }
    base_url = "https://prod.us-east-1.api.app-attestation.last-mile.amazon.dev/"
    url = f"{base_url}v1/android/register-attestation"
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 403:
        authCycle.header_refresh()
        authCycle.requestId_refresh()
        headers = header_data.headers.copy()
        attestation_header_refresh(headers)
        headers['X-Amzn-Identity-Auth-Domain'] = '.amazon.com'
        response = requests.post(url, headers=headers, json=data)
    if response.status_code != 200:
        print(f"Error sending request to register-attestation. Status code: {response.status_code}")
        try:
            debug_info = response.json()
        except:
            debug_info = response.text
        print(debug_info)
        exit()
    response_json = response.json() 
    new_key_id: str = response_json.get('keyId')
    expiration: int = response_json.get('expiration')
    key_id["keyId"] = new_key_id
    key_id["expiration"] = expiration
    with open("userdata/key_id.py", "w") as f:
        f.write(f'keyId="{new_key_id}"\n')
        f.write(f'expiration={expiration}\n')