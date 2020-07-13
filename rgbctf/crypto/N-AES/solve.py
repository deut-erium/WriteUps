from pwn import remote
from base64 import b64encode, b64decode
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from random import seed, randint
import re
from pwn import context
#context.log_level = "DEBUG"
HOST, PORT = "challenge.rgbsec.xyz", 34567
REM = remote(HOST, PORT)

CHALL = b64decode(REM.recvline().strip())
def rand_block(byte):
    """random block for given seed byte"""
    seed(byte)
    return bytes([randint(0,255) for _ in range(16) ])

KEYS = [rand_block(bytes([i])) for i in range(256)]
REM.recvuntil(b'\n>')
def enc_serv(plaintext, seed_bytes):
    REM.sendline(b'1')
    REM.sendline(b64encode(plaintext))
    REM.sendline(b64encode(seed_bytes))
    data = REM.recvuntil(b'\n>')
    encd = re.search(b'b\'([a-zA-Z0-9\+/]+)\'',data)[1]
    return b64decode(encd)

def dec_serv(ciphertext, seed_bytes):
    REM.sendline(b'2')
    REM.sendline(b64encode(ciphertext))
    REM.sendline(b64encode(seed_bytes))
    data = REM.recvuntil(b'\n>')
    if b'Error' not in data:
        decd = re.search(b'b\'([a-zA-Z0-9\+/]+)\'',data)[1]
        return b64decode(decd)

def decrypt(ct):
    ct_orig = ct
    for i in range(256):
        ct = ct_orig
        for _ in range(128):
            ct = AES.new(rand_block(bytes([i])),1).decrypt(ct)
        try:
            return unpad(ct,16)
        except:
            continue

REM.sendline(b'3')
REM.sendline(b64encode(decrypt(CHALL)))
print(REM.recvregex(b'rgbCTF{.*}').decode())
