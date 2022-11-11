#!/usr/bin/env python3
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from hashlib import md5
import sys

from secret import AES_KEY, FLAG

# AES.new(AES_KEY, AES.MODE_CBC, md5(AES_KEY).digest()).encrypt(pad(FLAG,16)).hex()

# b573a096bf6f525498eb19d297eb95e534fd997eb03ba2a1259a22f2d4d9e4a421d6765fb3c5e26fe5aa2ba8448aa06ac229ae5e0292d3544951027ce8acb47f

class Unbuffered(object):
   def __init__(self, stream):
       self.stream = stream

   def write(self, data):
       self.stream.write(data)
       self.stream.flush()

   def writelines(self, datas):
       self.stream.writelines(datas)
       self.stream.flush()

   def __getattr__(self, attr):
       return getattr(self.stream, attr)


sys.stdout = Unbuffered(sys.stdout)


class Strings:
    def __init__(self,line):
        self.line = line
        self.color_green = '\x1b[32m'
        self.color_red = '\x1b[31m'
        self.color_reset = '\x1b[0m'
        self.non_hex = self.color_red + f"ValueError: " + self.color_reset + \
                                                    f"non-hexadecimal number found!"
        self.bye = self.color_red + \
                    f"Out[{self.line}]: " + self.color_reset + "bye."
        self.input = self.color_green + f"In [{self.line}]: " + self.color_reset
        self.error = self.color_red + 'ErrorOccurred: ' + self.color_reset
        self.invallid_pad = self.color_red + \
            f"Out[{self.line-1}]: " + "Invalid Padding" + self.color_reset
        self.decrypted = self.color_red + f"Out[{self.line-1}]: " +     \
        self.color_green + "Successfully Decrypted" + self.color_reset
        


class Challenge:
    
    def __init__(self):
        self.line = 1
        self.str = lambda : Strings(self.line)
        self.aes_decrypt = \
            AES.new(AES_KEY, AES.MODE_CBC, md5(AES_KEY).digest()).decrypt


    def unpad(self, data):
        pad_byte = data[-1]
        return int( all([
            len(data) % 16 == 0,
            pad_byte <= 16,
            pad_byte >= 1,
            data[-pad_byte:] == bytes([pad_byte] * pad_byte)
        ]))

            
    def input(self):
        try:
            data = input(self.str().input)
        except:
            print()
        if data == 'exit':
            print(self.str().bye)
            sys.exit(0)
        else:
            try:
                data = bytes.fromhex(data)
            except:
                print(self.str().non_hex)
            self.line += 1
            return self.aes_decrypt(data)
                

    def run(self):
        try:
            plaintext = self.input()
            return [
                self.str().invallid_pad,
                self.str().decrypted
            ][self.unpad(
                plaintext
            )]
        except Exception as e:
            print(self.str().error,end='')
            print(e)
            raise KeyboardInterrupt


if __name__ == '__main__':

    challenge = Challenge()

    while True:
        try:
            print(challenge.run())
        except:
            break
    sys.exit()


