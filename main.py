import requests, json, time, logging, random
from datetime import datetime, date
import header_data
import json_data
import authCycle, getServiceAreas
import os
from amz_request import amz_request
from urllib.parse import urlparse, parse_qs

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
    
from yagmail_alert import Yagmail

import filters, live_updates, debug

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

try:
    import userdata.speed_behavior_values as sbv
except:
    print("Please set your speeds and rate limit sleep")
    exit()

import traceback

timehigh = sbv.timehigh
timelow = sbv.timelow

rapidvalue = sbv.rapidvalue

rapidtimehigh = sbv.rapidtimehigh
rapidtimelow = sbv.rapidtimelow

rapidrefresh = rapidvalue

#In Minutes
ratelimitsleep = sbv.ratelimitsleep

def rate_sleep_print():
    with open ("scandata/token-status", "a") as d:
        print('Rate Sleep Start at:', file=d)
        print(time.strftime('%m/%d/%Y %I:%M:%S %p'), file=d)
        print('------------------------------------', file=d)

def rate_wake_print():
    with open ("scandata/token-status", "a") as d:
        print('Rate Sleep End, at:', file=d)
        print(time.strftime('%m/%d/%Y %I:%M:%S %p'), file=d)
        print('------------------------------------', file=d)

logging.basicConfig(format="%(asctime)s \n\t%(message)s", datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)

session = requests.Session()

print('Scanning started at', time.strftime('%I:%M:%S %p'))

def get_offer_list(rejected_ids: set):
    global session
    start = time.time()
    response = amz_request(
        method="post", 
        url="https://flex-capacity-na.amazon.com/GetOffersForProviderPost",
        json=json_data.search_json_data,
        session=session
    )
    if response.status_code != 200:
        try:
            j = json.loads(response.text)
        except:
            j = None
        with open ("debugging/test", "a+") as t:
            if j:
                if "message" in j:
                    print(f"{time.strftime('%I:%M:%S %p')}, {j}", file=t)
                elif 'Message' in j:
                    msg = j['Message']
                    first_word = msg.split()[0] if msg else ''
                    if first_word == 'before':
                        print(f"{time.strftime('%I:%M:%S %p')}, {'Message: TokenException'}", file=t)
                    else:
                        print(f"{time.strftime('%I:%M:%S %p')}, {j}", file=t)
            else:
               print(f"{time.strftime('%I:%M:%S %p')}, Status code: {response.status_code}, {response.text}", file=t) 
        return []
    j = json.loads(response.text)
    #print(f"Time to get offer list response: {time.time() - start}")
    offer_accepted = False

    try:
        start = time.time()
        current_time = int(start)
        for block in j["offerList"]:
            if block['serviceAreaId'] in rejected_ids:
                continue
            block_in_list = block['serviceAreaId'] in filters.station_list
            if block_in_list:
                headstart = filters.time_headstart(block, current_time)
                adv_filter = filters.advanced_filter(block)
            else:
                headstart = True
                adv_filter = True
            if block_in_list and headstart and adv_filter and not block["hidden"]:
                status = accept_block(block)
                if status == 200:
                    offer_accepted = True
                    break
            else:
                rejected_ids.add(block['serviceAreaId'])
            #list_format(block)
            l_mode(block, block_in_list, headstart, adv_filter)
        #print(f"Processing time: {time.time() - start}")
    except KeyError:
        try:
            return j["message"]
        except KeyError:
            print('Disconnected.........', end='\r')
            raise
    return [200] if offer_accepted else []


def list_format(block):
    block_length = (block["endTime"] - block["startTime"]) / 3600
    block_price = block["rateInfo"]["priceAmount"]
    block_rate = block_price / block_length
    block_scheduled_time = date.fromtimestamp(block['startTime']).strftime('%A'), time.strftime('%m/%d/%Y %I:%M %p', time.localtime(block['startTime']))
    try:station_name = stationlist[block['serviceAreaId']]
    except:station_name = [block['serviceAreaId']]
    block_totals = round(block_rate, 2), 'x', round(block_length, 1), '=', round(block_price, 1)
    if block['offerType'] == 'EXCLUSIVE':reserved = '* * R E S E R V E D * *\n'
    else: reserved = '\r'
    print(
        f"{reserved}"
        f"{block_scheduled_time}\n"
        f"{station_name}\n"
        f"{block_totals}\n"
        f"{time.strftime('%m/%d/%Y %I:%M:%S %p')}\n"
        f"{reserved}"
        f'------------------------------------'
    )

def live_update_code(block):
    if(rapidrefresh>=rapidvalue):
        l_mode(block)
    if(rapidrefresh<rapidvalue):
        pass

def l_mode(block, block_in_list, headstart, adv_filter):
    if block_in_list:
        if not block["hidden"]:
            b_length = (block["endTime"] - block["startTime"]) / 3600
            b_price = block["rateInfo"]["priceAmount"]
            b_rate = b_price / b_length
            if headstart and not adv_filter and b_rate > 18:
                debug.scan_print(block)
            if adv_filter and not headstart:
                debug.nheadstart_print(block)
        if filters.baserate_filter(block):
            debug.baserate_print(block)
#    if block['serviceAreaId'] not in filters.station_list:
#        if b_rate > 18:
#            debug.baserate_print(block)
    
def l_rapid(block):
    if block['serviceAreaId'] in filters.station_list:
        if filters.advanced_filter(block) and filters.time_headstart(block, int(time.time())):
            live_updates.live_rapid(block)
            live_updates.rapid_history(block)

def lm_base(block):
    if filters.baserate_filter(block):
        debug.baserate_print(block)


def accept_block(block):
    # Accepting a block, returns status code. 200 is a successful attempt and 400 (I think, could be 404 or something else) is a failed attempt
    global session
    global rapidrefresh
    accept = amz_request(
        method="post", 
        url="https://flex-capacity-na.amazon.com/AcceptOffer",
        json=json_data.accept_json_data(block["offerId"]),
        session=session
    )

    if accept.status_code == 200:
        live_updates.live_mode(block)
        live_updates.print_history(block)
        logging.info(f"Caught The Block For {block['rateInfo']['priceAmount']}")
        debug.caught_print(block)
        try:
            yagmail = Yagmail()
            yagmail.email_alert(block)
        except:
            pass
    elif accept.status_code == 307:
        print("[+] Captcha challenge detected! Please follow the URL below and solve the challenge to continue:")
        url = accept.json()['challengeMetadata']['WebUrl']
        print(url)
        input_accepted = False
        validation_id = None
        while not validation_id:
            while not input_accepted:
                validation_url = input("Paste the URL which results from completing the Captcha. It contains the phrase 'uniqueValidationId': ")
                if "uniqueValidationId" in validation_url:
                    input_accepted = True
                else:
                    print("The URL does not contain the uniqueValidationId. Please try again.")
            try:
                parsed_query = parse_qs(urlparse(validation_url).query)
                j = json.loads(parsed_query['sessionToken'][0])
                validation_id = j['uniqueValidationId']
            except:
                print("The URL does not match the expected format. Please try again.")
                input_accepted = False
        validated = validate_captcha(validation_id)
        if not validated:
            exit() #TODO
        
    else:
        if(rapidrefresh>=rapidvalue):
            live_updates.live_mode(block)
            live_updates.print_history(block)
        if(rapidrefresh<rapidvalue):
            live_updates.live_rapid(block)
            live_updates.rapid_history(block)
        logging.info(f"Missed The Block For {block['rateInfo']['priceAmount']}")
        debug.missed_print(block)
        rapidrefresh = 0

    return accept.status_code

def validate_captcha(validationId: str) -> bool:
    data = {
        "challengeToken": f'{{"uniqueValidationId":"{validationId}"}}'
    }
    res = amz_request(
        method="post",
        url="https://flex-capacity-na.amazon.com/ValidateChallenge",
        json=data,
        session=session
    )
    if res.status_code == 200:
        print("Captcha verified!")
        return True
    else:
        print(f"Error validating captcha. Code {res.status_code}, Message: {res.text}")
        return False

def file_age_in_seconds(pathname):
    """
    Return the age of the file at pathname in seconds.
    """
    return time.time() - os.stat(pathname).st_mtime

def check_header_file():
    header_file = "userdata/access_token"
    if os.path.exists(header_file):
        age_in_seconds = file_age_in_seconds(header_file)
        if age_in_seconds > (59 * 60) + 50:
            print("Token is older than an hour")
            authCycle.request_print()
            authCycle.header_refresh()
        else:
            pass
    else:
        raise Exception('Token does not exist')

if __name__ == "__main__":

    authCycle.authCycle()
    authCycle.instanceCycle()
    authCycle.areaIdCycle()

    keepItUp = True
    rejected_ids = set()
    while keepItUp:
        print('Scanning...', datetime.now().strftime('%S:%f'), end='\r')
        check_header_file()
        try:
            lst = get_offer_list(rejected_ids)
        except:
            #traceback.print_exc()
            authCycle.authCycle()
            lst = get_offer_list(rejected_ids)
        if lst == "Rate exceeded":
            logging.info("Rate Exceeded, Waiting")
            rate_sleep_print()
            time.sleep(ratelimitsleep*60)
            logging.info("Resuming operations")
            rate_wake_print()
            authCycle.authCycle()
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
