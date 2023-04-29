import requests

def get_flex_version():
    session = requests.Session()
    host = "https://logistics.amazon.com"
    url = host + "/app/download-app-direct/android"
    headers = {
        "Host": host[8:],
        "Connection": "keep-alive",
        "sec-ch-ua-platform": "Android",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Linux; Android 13; SM-G998U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Mobile Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Dest": "document",
        "Referer": "https://logistics.amazon.com/app/download-app",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.9"
    }
    res = session.get(url, headers=headers)
    version_index = res.text.find("AmazonFlex")
    if version_index == -1:
        print("Error retrieving flex app version")
        print("Response status code: " + str(res.status_code))
        print("Response text: " + res.text)
    version = res.text[version_index + 11:]
    end_version_index = version.find("-")
    version = version[:end_version_index]
    if not version.upper().isupper():
        f = open("userdata/version", "w")
        f.write(version)
        f.close()
        return version
    else:
        print("Error retrieving flex app version")
        print("Version: " + version)