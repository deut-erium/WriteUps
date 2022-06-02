import pwn
from Crypto.Cipher import AES
import os
import random
import time

HOST, PORT = '01.cr.yp.toc.tf', 27010

def get_enc_flag():
    REM = pwn.remote(HOST, PORT)
    REM.recvuntil(b'[Q]uit\n')
    REM.sendline(b'g')
    enc_flag_data = REM.recvuntil(b'[Q]uit\n')
    enc_flag = pwn.re.search(b'= ([a-f0-9]+)\n',enc_flag_data)[1]
    enc_flag = bytes.fromhex(enc_flag.decode())
    REM.close()
    return enc_flag

enc_flag = get_enc_flag()
passphrase = b'HungryTimberWolf'

def encrypt(msg, passphrase, niv):
    aes = AES.new(passphrase, AES.MODE_GCM, nonce=niv)
    enc = aes.encrypt_and_digest(msg.encode('utf-8'))[0]
    return enc

key_streams = [encrypt('\x00'*100,passphrase,bytes([i])) for i in range(256)]

while True:
    for ks in key_streams:
        m = pwn.xor(enc_flag,ks)
        if m.startswith(b'EPOCH:'):
            print(m)
            exit(0)
    else:
        enc_flag = get_enc_flag()


# CCTF{____w0lveS____c4n____be____dan9er0uS____t0____p3oplE____!!!!!!}
