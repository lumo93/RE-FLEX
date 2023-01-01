search_json_data = {
    'apiVersion': 'V2',
    'filters': {
        'serviceAreaFilter': [
        ], 
        "timeFilter": {
            #"endTime": "23:00",
            #"startTime": "11:00"
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
