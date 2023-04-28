import header_data
import json_data
import getServiceAreas
import time
import uuid
from uuid import UUID
import registerCycle
import register
import os


refresh_token = registerCycle.rCycle()

def header_refresh():
    new_token = register.refresh(refresh_token)
    header_data.headers['x-amz-access-token'] = new_token

def current_header():
    with open("userdata/access_token", "r") as t:
        token = t.read()
        header_data.headers['x-amz-access-token'] = token

def requestId_refresh():
    header_data.headers['X-Amzn-RequestId'] = requestIdSelfSingleUse()
    header_data.headers['X-Flex-Client-Time'] = str(round(time.time() * 1000))

def manual_token():
        token = manualTokenRefresh()
        header_data.headers['x-amz-access-token'] = token
        with open('userdata/access_token', 'w') as t:
            print(token, end='', file=t)

def test():
    lst = getServiceAreas.getEligibleServiceAreas()
    if None in lst:
        print('Token expired........', end='\r')
        time.sleep(1)
        raise Exception
    else:
        pass

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
            request_print()
            header_refresh()
        else:
            current_header()
            test()
    else:
        print("Creating new token")
        raise


def authCycle():
    try:
        print('Reading from file ...', end='\r')
        time.sleep(1)
        check_header_file()
    except:
        try:
            request_print()
            header_refresh()
            test()
        except:
            blocked_print()
            manual_token()


def instance_check():
    with open("userdata/instance_id", "r") as i:
        instanceId = i.read()
    header_data.headers['x-flex-instance-id'] = instanceId

def instance_make():
    with open("userdata/instance_id", "w") as i:
        instanceId = str(uuid.uuid4())
        print(instanceId, end='', file=i)

def instanceCycle():
    try:
        instance_check()
    except:
        instance_make()
        instance_check()

def areaId_check():
    with open("userdata/areaId", "r") as i:
        areaId = i.read()
        return(areaId)

def areaId_grab():
    with open("userdata/areaId", "w") as i:
        areaId = getServiceAreas.getEligibleServiceAreas()[0]
        print(areaId, end='', file=i)

def areaIdCycle():
    try:
        areaId = areaId_check()
    except:
        areaId_grab()
        areaId = areaId_check()
    json_data.search_json_data["serviceAreaIds"] = [areaId]



def uuid_to_hex(uuid):
    return UUID(uuid).hex

def uuid_make():
    return(str(uuid.uuid4()))

def requestIdSelfSingleUse():
    return (
        str(uuid.uuid4())
    )

def manualTokenRefresh():
    token = input('Enter Access Token  :')
    return(token)

def request_print():
    time.sleep(1)
    with open ("scandata/token-status", "a") as d:
        print('Token request at:', file=d)
        print(time.strftime('%m/%d/%Y %I:%M:%S %p'), file=d)
        print('------------------------------------', file=d)
    print('Requesting token ....', end='\r')

def blocked_print():
    with open ("scandata/token-status", "a") as d:
        print('Token request blocked:', file=d)
        print(time.strftime('%m/%d/%Y %I:%M:%S %p'), file=d)
        print('------------------------------------', file=d)
    print(
        'Authentication rejected'
        )