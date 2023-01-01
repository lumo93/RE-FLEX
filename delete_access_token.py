import os

try:
    # Delete the file
    os.remove("userdata/access_token")
    print('File removed successfully')
except FileNotFoundError:
    # File does not exist, do nothing
    print('There is no file')
    pass
