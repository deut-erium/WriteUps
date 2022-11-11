from pwn import remote, re, context
from json import dumps, loads
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Util.number import getPrime, long_to_bytes
import hashlib

from fastecdsa.curve import secp256k1
from fastecdsa.point import Point
import random

CURVE = secp256k1
ORDER = CURVE.q
G = CURVE.G

private_key = -1
public_key = G*private_key
nonce = random.randint(2**65,2**80)

context(log_level=000)
HOST, PORT = "134.122.111.232", 54321
REM = remote(HOST,PORT)

alice_pk = REM.recvuntil('Send to Bob:')
alice_pk = loads( re.search(b'\{.*\}',alice_pk)[0] )
alice_pk = Point(alice_pk['Px'],alice_pk['Py'],curve=secp256k1)
REM.sendline( dumps({"Px": public_key.x,"Py":public_key.y,"nonce":nonce}) )

bob_pk = REM.recvuntil('Send to Alice:')
bob_pk = loads( re.search(b'\{.*\}',bob_pk)[0] )

bob_pk = Point(bob_pk['Px'],bob_pk['Py'],curve=secp256k1)

nonce2 = ((-alice_pk).x)^( (-bob_pk).x )^nonce

REM.sendline( dumps({"Px": public_key.x,"Py":public_key.y,"nonce":nonce2 } ) )

flag_data = REM.recvall()
flag_data = loads(re.search(b'\{.*\}',flag_data)[0])
iv = bytes.fromhex(flag_data['iv'])
enc_flag = bytes.fromhex(flag_data['encrypted_flag'])

shared_secret = ((-bob_pk).x)^nonce
key = hashlib.sha1(long_to_bytes(shared_secret)).digest()[:16]
cipher = AES.new(key,AES.MODE_CBC,iv)
pt = cipher.decrypt(enc_flag)

#union{https://buttondown.email/cryptography-dispatches/archive/cryptography-dispatches-the-most-backdoor-looking/}

