#!/usr/sbin/python
from secret import flag
from Crypto.Cipher import AES
from os import urandom

key=urandom(16)

def encrypt(msg, iv):
    cipher = AES.new(key, AES.MODE_OFB,iv)
    ct = cipher.encrypt(msg)
    return ct if ct not in flag else b"try_harder"

def main():
    print('Welcome to inctf.\nHere is a gift from my side:')
    iv=urandom(16)
    print(iv.hex()+encrypt(flag,iv).hex())
    print("You can encrypt any string you want 3 times.")
    for _ in range(3):
        x=bytes.fromhex(input("> ").strip())
        iv,msg=x[:16],x[16:]
        print(encrypt(msg,iv).hex())

if __name__=='__main__':
    main()