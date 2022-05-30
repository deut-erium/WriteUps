from pwn import remote, re, context
import string
CHARSET = string.printable[:94].encode()
from Crypto.Util.number import long_to_bytes, bytes_to_long
import hashlib
context.log_level = 20
HOST, PORT = "simple-service-c45xrrmhuc5su.shellweplayaga.me", 31337

TICKET = "ticket{WaterlineShip4043n22:GIynTTVeYakSTLxReEq1h87DYOPqdqoEb13pJh8whFkf_Mfy}"

REM = remote(HOST, PORT)
REM.recvuntil(b": ")
REM.sendline(TICKET)

data = REM.recvuntil(b" =")
REM.sendline(str(eval(data.split(b' =')[0])))
print(REM.recvall())
