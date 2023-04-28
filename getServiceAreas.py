from datetime import datetime
import header_data
from amz_request import amz_request


def __getAmzDate() -> str:
    """
        Returns Amazon formatted timestamp as string
        """
    return datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')

def getEligibleServiceAreas():

    header_data.headers["X-Amz-Date"] = __getAmzDate()
    response = amz_request(
        method="get", 
        url="https://flex-capacity-na.amazon.com/eligibleServiceAreas"
    )
    return response.json().get("serviceAreaIds")

def getAllServiceAreas():

    header_data.headers["X-Amz-Date"] = __getAmzDate()
    serviceAreaPoolList = amz_request(
        method="get", 
        url="https://flex-capacity-na.amazon.com/getOfferFiltersOptions"
    ).json().get("serviceAreaPoolList")
    with open("userdata/serviceAreaIds", "w", encoding='utf-8') as s:
        #print('stationlist = {', file=s)
        for serviceArea in serviceAreaPoolList:
            Name = serviceArea["serviceAreaName"]
            ID = serviceArea["serviceAreaId"]
            print('{1}:{0}'.format(Name, ID), file=s)
        #print('}', file=s)