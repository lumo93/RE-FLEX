import register

def load_data(filepath):
    with open(filepath, 'r') as f:
        data = f.read()
    return data

def rCycle():
    try:
        with open("userdata/refresh_token", "r") as r:
            rt = r.read()
            return(rt)
    except:
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