import pwn

HOST, PORT = "crypto.2021.chall.actf.co", 21602

REM = pwn.remote(HOST,PORT)

def get_encryption(pt:bytes):
    REM.recvuntil(b'?') # what would you like to do
    REM.sendline(b'1')
    REM.sendline(pt.hex())
    encrypted = REM.recvline().strip().split(b': ')[1]
    return bytes.fromhex(encrypted.decode())

def enc(x,k1,k2,k3):
    encr = (not x) and k1
    encr = (not encr) and k2
    encr = (not encr) and k3
    return encr

