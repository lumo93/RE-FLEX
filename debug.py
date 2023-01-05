import time
from datetime import date

def load_data(filepath):
    with open(filepath, 'r') as f:
        data = f.read()
    stationlist = {}
    for line in data.splitlines():
        station_id, station_name = line.split(':')
        stationlist[station_id] = station_name
    return stationlist

stationlist = load_data('userdata/serviceAreaIds')

def print_format(block, f):
    block_length = (block["endTime"] - block["startTime"]) / 3600
    block_price = block["rateInfo"]["priceAmount"]
    block_rate = block_price / block_length
    if block['offerType'] == 'EXCLUSIVE':print('* * R E S E R V E D * *', file=f)
    print(date.fromtimestamp(block['startTime']).strftime('%A'), time.strftime('%m/%d/%Y %I:%M %p', time.localtime(block['startTime'])), file=f)
    try:
        print(stationlist[block['serviceAreaId']], file=f)
    except:
        print([block['serviceAreaId']], file=f)
    print(round(block_rate, 2), 'x', round(block_length, 1), '=', round(block_price, 1), file=f),
    print(time.strftime('%m/%d/%Y %I:%M:%S %p'), file=f)
    if block['offerType'] == 'EXCLUSIVE':print('* * R E S E R V E D * *', file=f)
    print('------------------------------------', file=f)
    

def scan_print(block):
    try:
        with open ("scandata/Offers_Outside_Filters", "a") as f:
            print_format(block, f)
    except KeyError:
        print('scan print glitch')
        
def baserate_print(block):
    try:
        with open ("scandata/Baserate", "a") as f:
            print_format(block, f)
    except KeyError:
        print('baserate print glitch')

def nheadstart_print(block):
    try:
        with open ("scandata/Starts_Too_Soon", "a") as f:
            print_format(block, f)
    except KeyError:
        print('nheadstart print glitch')

def caught_print(block):
        with open("scandata/Recent_Attempts", "a") as f:
            print('Caught Block for', round(block['rateInfo']['priceAmount'], 1), 'Dollars', file=f)
            print('----------------------------------')

def missed_print(block):
        with open("scandata/Recent_Attempts", "a") as f:
            print('Missed Block for', round(block['rateInfo']['priceAmount'], 1), 'Dollars', file=f)
            print('----------------------------------')