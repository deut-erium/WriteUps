import pwn
import requests

HOST, PORT = "192.53.115.129",31339
REM = pwn.REMOTE(HOST, PORT)
# data={"recipient":"Casino","command":"Register","username":"loda"}
# r = requests.get(URL,data=data)

