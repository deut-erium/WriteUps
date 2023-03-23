

# pt0 pt1

# enc = E(nonce) || E(nonce+1) || E(nonce+2)

# E(nonce+1) ^ pt0 || E(nonce +2) ^ pt1

# TAG = E(nonce) ^ GHASH(E(0),ct)

# Hkey = E(0)

# E(0) || E(1) || E(2)

# E(1) || E(2)  E(0) ^ GHASH(E(0), E(1) || E(2))

import pwn
from Crypto.Util.number import *
HOST, PORT = "galois.wolvctf.io", 1337
REM = pwn.remote(HOST, PORT)
def GF_mult(x, y):
    product = 0
    for i in range(127, -1, -1):
        product ^= x * ((y >> i) & 1)
        x = (x >> 1) ^ ((x & 1) * 0xE1000000000000000000000000000000)
    return product

def H_mult(H, val):
    product = 0
    for i in range(16):
        product ^= GF_mult(H, (val & 0xFF) << (8 * i))
        val >>= 8
    return product

def GHASH(H, A, C):
    C_len = len(C)
    A_padded = bytes_to_long(A + b'\x00' * (16 - len(A) % 16))
    if C_len % 16 != 0:
        C += b'\x00' * (16 - C_len % 16)

    tag = H_mult(H, A_padded)

    for i in range(0, len(C) // 16):
        tag ^= bytes_to_long(C[i*16:i*16+16])
        tag = H_mult(H, tag)

    tag ^= bytes_to_long((8*len(A)).to_bytes(8, 'big') + (8*C_len).to_bytes(8, 'big'))
    tag = H_mult(H, tag)

    return tag

header = b'WolvCTFCertified'
message = b'heythisisasupersecretsupersecret'

REM.recvuntil(b'Exit\n\n')
REM.sendline(b'1')

REM.sendline(b'f'*32)
REM.sendline((bytes(16)+message).hex())

data = REM.recvuntil(b'Exit\n\n')
ct_hex = data.split(b'\n')[0].split(b'CT:  ')[1].decode()
ct = bytes.fromhex(ct_hex)

REM.sendline(b'2')
REM.sendline(b'0'*32)
REM.sendline(ct[16:].hex())
new_tag = long_to_bytes(bytes_to_long(ct[:16])^GHASH(bytes_to_long(ct[:16]),header,ct[16:])).hex()
REM.sendline(new_tag)

print(REM.recvuntil(b'\n\n'))
