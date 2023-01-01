import requests
from datetime import datetime
import header_data
import authCycle


def __getAmzDate() -> str:
    """
        Returns Amazon formatted timestamp as string
        """
    return datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')

def getEligibleServiceAreas():

    authCycle.requestId_refresh()
    header_data.headers["X-Amz-Date"] = __getAmzDate()
    response = requests.get(
    "https://flex-capacity-na.amazon.com/eligibleServiceAreas",
    headers=header_data.headers)
    return response.json().get("serviceAreaIds")

def getAllServiceAreas():

    authCycle.requestId_refresh()

    header_data.headers["X-Amz-Date"] = __getAmzDate()

    serviceAreaPoolList = requests.get(
    "https://flex-capacity-na.amazon.com/getOfferFiltersOptions",
    headers=header_data.headers
    ).json().get("serviceAreaPoolList")
    with open("userdata/serviceAreaIds", "w", encoding='utf-8') as s:
        #print('stationlist = {', file=s)
        for serviceArea in serviceAreaPoolList:
            Name = serviceArea["serviceAreaName"]
            ID = serviceArea["serviceAreaId"]
            print('{1}:{0}'.format(Name, ID), file=s)
        #print('}', file=s)