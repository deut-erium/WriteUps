#!/usr/bin/env python3

from random import *
from Crypto.Util.number import *
from fastecdsa.curve import secp256k1
from hashlib import *
import string
from flag import flag

def randstr(l):
	return ''.join([string.printable[:62][randrange(62)] for _ in range(l)])

def ecc_sign(msg, ecc, privkey):
	z = sha256(msg).hexdigest()
	k = int(z, 16) ^ privkey
	x, y = (k * ecc.G).x, (k * ecc.G).y
	r = x
	s = inverse(k, ecc.q) * (int(z, 16) + r * privkey) % ecc.q
	return (r, s)

def ecc_sing_verify(msg, sign, ecc, pubkey):
	r, s = sign
	assert (r < ecc.q and s < ecc.q)
	z = sha256(msg).hexdigest()
	u, v = int(z, 16) * inverse(s, ecc.q), r * inverse(s, ecc.q)
	R = u * ecc.G + v * pubkey
	return r == R.x

ecc = secp256k1
privkey = randrange(ecc.q)
pubkey = privkey * ecc.G

for _ in range(313):
	msg = randstr(40).encode()
	sign = ecc_sign(msg, ecc, privkey)
	print(f'{msg}, {sign}, {ecc_sing_verify(msg, sign, ecc, pubkey)}')

d = bytes_to_long(flag.lstrip(b'CCTF{').rstrip(b'}'))
print(f'enc = {(d * ecc.G).x}')
