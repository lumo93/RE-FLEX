import yagmail
from datetime import date
import time

def load_data(filepath):
    with open(filepath, 'r') as f:
        data = f.read()
    stationlist = {}
    for line in data.splitlines():
        station_id, station_name = line.split(':')
        stationlist[station_id] = station_name
    return stationlist

stationlist = load_data('userdata/serviceAreaIds')

class Yagmail:

    def __init__(self) -> None:
        self.yag = yagmail.SMTP(user="second email", password="apppassword")


    def email_alert(self, block):
        block_length = (block["endTime"] - block["startTime"]) / 3600
        block_price = block["rateInfo"]["priceAmount"]
        block_rate = block_price / block_length
        block_start = f"{date.fromtimestamp(block['startTime']).strftime('%A')} {time.strftime('%m/%d/%Y %I:%M %p', time.localtime(block['startTime']))}"
        station_name = stationlist[block['serviceAreaId']]
        subject = f"Work Available at {station_name}"
        body = f"Pay: ${block_price}\nBlock Length: {block_length} hours\nRate: {round(block_rate, 2)}\nStart Time: {block_start}"
        self.yag.send(to='main email', subject=subject, contents=body)
