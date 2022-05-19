from pwn import remote
from hashlib import sha256
import re
import string
from itertools import permutations as take
from Crypto.Cipher import ARC4
from struct import pack, unpack
from pwn import *
context.log_level = 'debug'
CHARSET_SHA = string.printable[:62].encode()

HOST, PORT = "pwnable.org", 10001

REM = remote(HOST, PORT)

SHA_CHALL = REM.recvuntil(b'XXXX:')
#print(SHA_CHALL.decode())
SHA_256_HASH = re.search(b"[0-9a-f]{64}",SHA_CHALL).group(0).decode()
POSTFIX_STR = re.search(b"[0-9a-zA-Z]{16}",SHA_CHALL).group(0)

xs = (0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 1, 0, 1, 0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 1)
xs = [2*i for i in xs]

def pow_sha(postfix, hash_val):
    for prefix in take(CHARSET_SHA, 4):
        prefix_bytes = bytes(prefix)
        shaa = sha256(prefix_bytes+postfix).hexdigest() 
        if shaa == SHA_256_HASH:
            print(prefix_bytes)
            return prefix_bytes


PREFIX_CHALL = pow_sha(POSTFIX_STR, SHA_256_HASH)
REM.send(PREFIX_CHALL)
REM.recv()
REM.send(b'aaa') #message
for i in range(64):
    REM.send(str(xs[i]).encode()) #xi's
    REM.recv()
    
REM.send(b'0') #v
REM.recv()
REM.interactive()
#flag{babbbcbdbebfbgbhbibjbkblbmbnbobpbqbrbsbtbubvbwbxby}
