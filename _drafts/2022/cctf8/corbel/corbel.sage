#!/usr/bin/env sage

from flag import flag
from Crypto.Util.number import *

p, q = [next_prime(randint(0, 2**512)) for _ in '01']

n = p*q
pin = randint(2, 2**32)

m = bytes_to_long(flag)

e = 13711
c_1 = pow(m, e, n)
c_2 = pow(m + pin, e, n)

enc = str(n) + str(c_1) + str(c_2)

print(f'Decrypt me: {hex(int(enc))}')