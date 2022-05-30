import pwn
from Crypto.Util.number import bytes_to_long, inverse, long_to_bytes
from Crypto.Random import get_random_bytes
from Crypto.Random.random import randint
from Crypto.Protocol.KDF import scrypt
import hashlib, binascii

P = (1 << 1024) - 1093337
G = 7
IV = b"y3ll0w subm4r1n3"
HOST, PORT = "gc1.eng.run",31084
REM = pwn.remote(HOST, PORT)
# REM = pwn.process('python3 mtproto.py',shell=True)

def kdf(secret):
    password = long_to_bytes(secret)
    salt = IV
    pswd = binascii.hexlify(scrypt(password, salt, 16, N=2**14, r=8, p=1))
    key = binascii.hexlify(pswd[:16])
    return str(key)

def kdf(secret):
    password = long_to_bytes(secret)
    salt = IV
    pswd = scrypt(password, salt, 16, N=2**14, r=8, p=1)
    key = binascii.hexlify(pswd[:16])
    return str(key)

REM.sendline(str(G))
REM.sendline(str(G))

data = REM.recvuntil(b'send nonce value to Bob->')

numbs = pwn.re.search(b'.*Message from alice: (\d+)\n\nsend to Bob->\n\nMessage from bob: (\d+)\n\nsend to Alice->\n\nnonce send to Alice: (\d+)\n\nsend nonce value to Bob->',data).groups()
ma, mb, na = map(int,numbs)
REM.sendline(str(ma^mb^na))

secret = kdf(ma^na)
# REM.sendline(str(ma^na))
REM.sendline(secret)

print(REM.recvall())

