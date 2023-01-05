import requests, json, time, logging, random
from datetime import datetime, date
import header_data
import json_data
import authCycle, getServiceAreas
import os

if not os.path.exists("userdata/version"):
    print("Please set the current Android Flex app version!\nFollowed by the useragent!")
    exit()

if not os.path.exists("userdata/useragent"):
    print("Please set your useragent!")
    exit()

def load_data(filepath):
    with open(filepath, 'r') as f:
        data = f.read()
    stationlist = {}
    for line in data.splitlines():
        station_id, station_name = line.split(':')
        stationlist[station_id] = station_name
    return stationlist


try:
    stationlist = load_data('userdata/serviceAreaIds')
except:
    authCycle.authCycle()
    getServiceAreas.getAllServiceAreas()
    stationlist = load_data('userdata/serviceAreaIds')

import filters, live_updates, yagmail_alert, debug

keys = []

# open the file in read mode
with open('userdata/chosen_station_list', 'r') as f:
    # read each line in the file
    for line in f:
        # split the line on the colon character
        key, _ = line.split(':')
        # add the key to the list
        keys.append(key)

with open('userdata/useragent', 'r') as u:
    ua = u.read()
with open('userdata/version', 'r') as v:
    ver = v.read()

header_data.headers['User-Agent'] = f"'{ua} RabbitAndroid/{ver}'"
# update the value of serviceAreaFilter in search_json_data
json_data.search_json_data["filters"]["serviceAreaFilter"] = keys


timehigh = 4.2
timelow = 3.8

rapidvalue = 3

rapidtimehigh = 0.3
rapidtimelow = 0.2

rapidrefresh = rapidvalue

#In Minutes
ratelimitsleep = 30

logging.basicConfig(format="%(asctime)s \n\t%(message)s", datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)

session = requests.Session()

print('Scanning started at', time.strftime('%I:%M:%S %p'))

def get_offer_list():
    authCycle.requestId_refresh()
    global session
    response = session.post(
        "https://flex-capacity-na.amazon.com/GetOffersForProviderPost",
        headers=header_data.headers,
        json=json_data.search_json_data,
    )
    j = json.loads(response.text)
    offer_accepted = False
    try:
        for block in j["offerList"]:
            if(rapidrefresh>=rapidvalue):
                l_mode(block)
            if(rapidrefresh<rapidvalue):
                l_rapid(block)
            if block['serviceAreaId'] in filters.station_list and filters.time_headstart(block) and filters.advanced_filter(block) and not block["hidden"] and not offer_accepted:
                status = accept_block(block)
                if status == 200:
                    offer_accepted = True
                    break
    except KeyError:
        try:
            return j["message"]
        except KeyError:
            print('Disconnected.........', end='\r')
            raise
    return [200] if offer_accepted else []

def l_mode(block):
    b_length = (block["endTime"] - block["startTime"]) / 3600
    b_price = block["rateInfo"]["priceAmount"]
    b_rate = b_price / b_length
    if block['serviceAreaId'] in filters.station_list:
        if filters.time_headstart(block) and filters.advanced_filter(block) and not block["hidden"]:
            live_updates.live_mode(block)
            live_updates.print_history(block)
        if filters.time_headstart(block) and not filters.advanced_filter(block) and b_rate > 18 and not block["hidden"]:
            debug.scan_print(block)
        if filters.advanced_filter(block) and not filters.time_headstart(block) and not block["hidden"]:
            debug.nheadstart_print(block)
    if block['serviceAreaId'] not in filters.station_list:
        if b_rate > 18:
            debug.scan_print(block)
    lm_base(block)

def l_mode_lite(block):
    b_length = (block["endTime"] - block["startTime"]) / 3600
    b_price = block["rateInfo"]["priceAmount"]
    b_rate = b_price / b_length
    if block['serviceAreaId'] in filters.station_list:
        if filters.time_headstart(block) and filters.advanced_filter(block) and not block["hidden"]:
            live_updates.live_mode(block)
            live_updates.print_history(block)
    
def l_rapid(block):
    if block['serviceAreaId'] in filters.station_list:
        if filters.advanced_filter(block) and filters.time_headstart(block):
            live_updates.live_rapid(block)
            live_updates.rapid_history(block)

def lm_base(block):
    if filters.baserate_filter(block):
        debug.baserate_print(block)


def accept_block(block):
    # Accepting a block, returns status code. 200 is a successful attempt and 400 (I think, could be 404 or something else) is a failed attempt
    global session
    global rapidrefresh
    accept = session.post(
        "https://flex-capacity-na.amazon.com/AcceptOffer",
        headers=header_data.headers,
        json=json_data.accept_json_data(block["offerId"]),
    )

    if accept.status_code == 200:
        logging.info(f"Caught The Block For {block['rateInfo']['priceAmount']}")
        debug.caught_print(block)
        yagmail_alert.email_alert(block)
    else:
        logging.info(f"Missed The Block For {block['rateInfo']['priceAmount']}")
        debug.missed_print(block)
        rapidrefresh = 0

    return accept.status_code

if __name__ == "__main__":

    authCycle.instanceCycle()
    authCycle.authCycle()
    authCycle.areaIdCycle()

    keepItUp = True
    while keepItUp:
            print('Scanning...', datetime.now().strftime('%S:%f'), end='\r')
            try:
                lst = get_offer_list()
            except:
                authCycle.authCycle()
            if lst == "Rate exceeded":
                logging.info("Rate Exceeded, Waiting")
                time.sleep(ratelimitsleep*60)
                logging.info("Resuming operations")
            try:
                if 200 in lst:
                    keepItUp = False
                    quit()
            except:
                pass
            if(rapidrefresh<rapidvalue):
                rapidrefresh+=1
                time.sleep(random.uniform(rapidtimelow, rapidtimehigh))
            else:
                time.sleep(random.uniform(timelow, timehigh))
