import register
import os

def load_data(filepath):
    with open(filepath, 'r') as f:
        data = f.read()
    return data

def rCycle():
    try:
        if not os.path.exists("userdata/device_tokens.py"):
            raise Exception
        with open("userdata/refresh_token", "r") as r:
            rt = r.read()
            return(rt)
    except:
        register.create_and_save_attestation_keys()
        challengelinkstatic = register.challenge_link
        print(challengelinkstatic)
        maplanding_url = input('Enter result URL from doing Challenge Link:')
        refresh_token = register.register_account(maplanding_url)
        with open("userdata/refresh_token", "w") as r:
            rt = refresh_token
            print(rt, end='', file=r)
        with open("userdata/refresh_token", "r") as r:
            rt = r.read()
            return(rt)