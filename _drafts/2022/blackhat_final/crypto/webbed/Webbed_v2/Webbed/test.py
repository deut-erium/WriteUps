from app import *
from pwn import xor
import random
secret_key = os.urandom(32)
crypto = Crypto(secret_key)

token = bytes.fromhex(crypto.gen_token("ab"+"0"*16))
mask = xor(b'{"username": "ab',b'{"username":"","x')+bytes(16)+xor('", "admin": false','
mask = bytes(16+16+12)+xor(b"fals"," tru")+bytes(16)
token_new = xor(mask, token)
print(crypto.validate_token(token_new))
