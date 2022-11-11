from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import os

img = open('chall.bmp', 'rb')
cipher = AES.new(os.urandom(16), AES.MODE_ECB)

x = cipher.encrypt(pad(img.read(), 16))
open('chall.encrypted.bmp', 'wb').write(x)
