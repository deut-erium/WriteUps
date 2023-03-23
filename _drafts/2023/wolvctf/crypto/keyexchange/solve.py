from Crypto.Util.strxor import strxor
from Crypto.Util.number import *
import pwn

HOST, PORT = "keyexchange.wolvctf.io", 1337
REM = pwn.remote(HOST, PORT)

REM.sendline(b"1")

REM.recvline()
aa = int(REM.recvline().strip())

enc = bytes.fromhex(REM.recvline().split()[-1].decode())
print(strxor(enc, long_to_bytes(aa)))
