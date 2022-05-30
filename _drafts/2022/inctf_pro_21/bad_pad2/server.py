#!/usr/bin/env python3
from Crypto.Cipher import AES
from hashlib import md5
from json import loads
import sys

from secret import AES_KEY, FLAG



class Strings:
    def __init__(self,line):
        self.line = line
        self.color_green = '\x1b[32m'
        self.color_red = '\x1b[31m'
        self.color_reset = '\x1b[0m'
        self.non_hex = self.color_red + f"ValueError: " + self.color_reset + \
                                                    f"non-hexadecimal number found!\n"
        self.bye = self.color_red + \
                    f"Out [{self.line}]: " + self.color_reset + "bye."
        self.input = self.color_green + f"In [{self.line}]: " + self.color_reset
        self.error = self.color_red + 'ErrorOccurred: ' + self.color_reset
        self.invallid_pad = self.color_red + \
            f"Out [{self.line-1}]: " + "Invalid Padding" + self.color_reset + '\n'
        self.decrypted = self.color_red + f"Out [{self.line-1}]: " +     \
        self.color_green + "Successfully Decrypted" + self.color_reset + '\n'
        self.flag = self.color_red + f"Out [{self.line}]: " + self.color_reset + \
            "Hey Admin, Here is your Flag: " + FLAG + "\n"
        


class Challenge:
    
    def __init__(self):
        self.line = 1
        self.str = lambda : Strings(self.line)
        self.aes_decrypt = lambda data :  AES.new(AES_KEY, AES.MODE_CBC, data[:16]).decrypt(data[16:])


    def unpad(self, data):
        pad_byte = data[-1]
        valid = int( all([
            len(data) % 16 == 0,
            pad_byte <= 16,
            pad_byte >= 1,
            data[-pad_byte:] == bytes([pad_byte] * pad_byte)
        ]))
        if valid:
            try:
                unpacked = loads(data[:-pad_byte].decode())
                if unpacked['Admin']: return valid + 1
                else: return valid
            except:
                return valid
        else: return valid

            
    def input(self):
        data = input(self.str().input)
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
                self.str().decrypted,
                self.str().flag
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
