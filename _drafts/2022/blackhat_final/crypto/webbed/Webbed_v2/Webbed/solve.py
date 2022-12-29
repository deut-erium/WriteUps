import requests
from pwn import xor
from itertools import product
import random

URL = "http://127.0.0.1:5000/"
URL = "https://blackhat4-4689a3997b611d824e7f5a83a0fc7533-0.chals.bh.ctf.sa"
REGISTER_URL = URL+"register/ab"+"d"*16
LOGIN_URL = URL+"login/ab"
ALLOWED = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_'

s = requests.session()
r = s.get(REGISTER_URL)

token = bytes.fromhex(s.cookies['token'])
# mask = bytes(16+16+12)+xor(b"fals"," tru")+bytes(16)
mask = bytes(16+16)+os.urandom(12)+xor(b"fals"," tru")+bytes(16)

cookie = {"token":xor(token,mask).hex()}

for num in range(1):
    for p in product(ALLOWED,repeat=num):
        print(p)
        r = requests.get(LOGIN_URL+"".join(p),cookies=cookie)
        if "Successfully logged in" in r.text:
            print(cookie)
            print("".join(p))

    # m = mask+bytes([i])
    # token_new = xor(token,m)
