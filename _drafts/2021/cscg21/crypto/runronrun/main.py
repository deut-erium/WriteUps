#!/usr/bin/env python3

try:
    from Crypto.Cipher import ARC4
except:
    print("PyCryptoDome is not installed!")
    exit(1)

#from secret import FLAG
FLAG = b'hello world!!'
import os



def roncrypt_flag(offset):
    key = os.urandom(16)
    cipher = ARC4.new(key)
    return cipher.encrypt(FLAG[offset:])


def main():

    while True:
        offset = int(input("Enter Offset>"))
        
        if not (0 <= offset < len(FLAG)):
            print("Offset is not in allowed range!")
            exit(2)

        encryted_flag = roncrypt_flag(offset)
        print(encryted_flag.hex())


if __name__ == '__main__':
    main()
