try:
    import userdata.speed_behavior_values as time
except:
    print("Please set the Speeds and Behavior")
    exit()

start = time.starttime
end = time.endtime


search_json_data = {
    'apiVersion': 'V2',
    'filters': {
        'serviceAreaFilter': [
        ], 
        "timeFilter": {
            "endTime": end,
            "startTime": start
        }   
    },
    "serviceAreaIds": ['areaId']
}


def accept_json_data(offerID):
    # This is the json data needed to accept a block, it takes an argument to extract the offer ID for the selected block
    return {
        "__type": "AcceptOfferInput:http://internal.amazon.com/coral/com.amazon.omwbuseyservice.offers/",
        "offerId": offerID,
    }
