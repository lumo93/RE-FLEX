import time
try:
    import userdata.station_filter_values as station_filter_values
    station_list = station_filter_values.station_list
except:
    raise Exception('Please choose stations and set filter values:')


def simple_filter(block):
    # Filtering out blocks that you don't want.
    # Comment out individual filters that you don't want applied
    b_length = (block["endTime"] - block["startTime"]) / 3600
    b_price = block["rateInfo"]["priceAmount"]
    b_headstart = block["startTime"] - int(time.time())
    b_rate = b_price / b_length
    return (
        b_rate > 18
        #and b_price > 110
        #and b_headstart >= 1500
        #and b_length < 5
    )

def baserate_filter(block):
    # Comment out the second line if you want to print base rate
    b_length = (block["endTime"] - block["startTime"]) / 3600
    b_price = block["rateInfo"]["priceAmount"]
    #b_headstart = block["startTime"] - int(time.time())
    b_rate = b_price / b_length
    return (
        b_rate == 18
    )

#advanced filters

def advanced_filter(block):
    b = station_list[block['serviceAreaId']]
    lowprice = b['lowprice']
    minlength = b['minlength']
    maxlength = b['maxlength']
    rate = b['rate']
    b_length = (block["endTime"] - block["startTime"]) / 3600
    b_price = block["rateInfo"]["priceAmount"]
    b_rate = b_price / b_length
    if b_price < lowprice:
        if maxlength >= b_length >= minlength:
            return (
                b_rate >= rate
            )
    else:
        return(
            b_price >= lowprice
        )

def time_headstart(block, current_time: int):
    b = station_list[block['serviceAreaId']]
    headstart = b['headstart']
    b_headstart = block["startTime"] - current_time
    return(
        b_headstart >= headstart*60
    )