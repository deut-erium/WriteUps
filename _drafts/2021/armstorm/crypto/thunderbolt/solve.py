import pwn

import os
HOST, PORT = "crypto.2021.chall.actf.co" ,21603

def get_enc(inp:bytes):
    REM = pwn.remote(HOST,PORT)
    REM.sendline(inp)
    enc = REM.recvline().strip().split(b': ')[-1].decode()
    REM.close()
    return bytes.fromhex(enc)

def get_enc_local(inp:bytes):
    REM = pwn.process('./chall')
    REM.sendline(inp)
    enc = REM.recvline().strip().split(b': ')[-1].decode()
    REM.close()
    return bytes.fromhex(enc)


def encrypt(flag, key_16=os.urandom(16)):
    f = [i for i in range(256)]
    t=0x00
    leng = len(flag)
    encrypted = [0]*leng
    full_key = os.urandom(leng)
    for i in range(768):
        t = f[(f[i%256]+t+full_key[ i%leng])%256]
        f[i%256],f[t] = f[t],f[i%256]

    for i in range(768):
        t = f[(f[i%256]+t+key_16[i%16])%256]
        f[i%256],f[t] = f[t],f[i%256]

    for i in range(leng):
        t = f[(f[i%256]+t)%256]
        encrypted[i] = flag[i] ^ f[(f[f[t]]+1)%256] 
        f[t],f[(i+1)%256] = f[(i+1)%256],0
    return encrypted

