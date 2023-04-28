import requests, authCycle
import header_data

def amz_request(method: str, url: str, json: dict=None, session: requests.Session=None) -> requests.Response:
    if session:
        req = session.get if method == "get" else session.post
    else:
        req = requests.get if method == "get" else requests.post
    authCycle.requestId_refresh()
    res = req(url, headers=header_data.headers, json=json)
    if res.status_code == 403:
        authCycle.header_refresh()
        authCycle.requestId_refresh()
        res = req(url, headers=header_data.headers, json=json)
    return res