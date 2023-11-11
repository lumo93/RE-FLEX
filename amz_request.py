import requests, authCycle
import header_data
import signature_headers

def amz_request(method: str, url: str, json: dict=None, session: requests.Session=None, sign_request=False) -> requests.Response:
    if session:
        req = session.get if method == "get" else session.post
    else:
        req = requests.get if method == "get" else requests.post
    authCycle.requestId_refresh()
    headers = header_data.headers.copy()
    if sign_request:
        headers.update(signature_headers.signature_headers)
    res = req(url, headers=headers, json=json)
    if res.status_code == 403:
        authCycle.header_refresh()
        authCycle.requestId_refresh()
        headers = header_data.headers.copy()
        if sign_request:
            headers.update(signature_headers.signature_headers)
        res = req(url, headers=headers, json=json)
    return res