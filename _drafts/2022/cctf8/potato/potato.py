#!/usr/bin/env python3

from random import *
from Crypto.Util.number import *
from fastecdsa.curve import *
from flag import flag


def ecc_gen(nbit):
    while True:
        p = getPrime(nbit)
        if p % 4 == 3:
            a, b = [randrange(p) for _ in '01']
            x = randrange(p)
            y2 = (x**3 + a * x + b) % p
            assert y2 % p == (x**3 + a * x + b) % p
            if pow(y2, (p - 1) // 2, p) == 1:
                y = pow(y2, (p + 1) // 4, p)
                break
    return Curve('CCTF', p, a, b, None, x, y)


def encrypt(m, ecc):
    y = hex(int.from_bytes(m, 'big'))[2:]
    if len(y) % 2 == 1:
        y = '0' + y
    Y = [y[2 * i:2 * i + 2] for i in range(len(y) // 2)]
    k, s = [randrange(ecc.p) for _ in '01']
    s = pow(ecc.G.x, ecc.G.y, ecc.p)
    c_0 = k * ecc.G
    e = k * s * ecc.G
    C = [(c_0.x, c_0.y)]
    for y in Y:
        y_1 = (e.x * int(y[0], 16)) % ecc.p
        y_2 = (e.y * int(y[1], 16)) % ecc.p
        C.append((y_1, y_2))
    return C


ecc = ecc_gen(256)
enc = encrypt(flag, ecc)

print(f"n = {ecc.p}")
print(f"a = {ecc.a}")
print(f"b = {ecc.b}")
print(f"enc = {enc}")
