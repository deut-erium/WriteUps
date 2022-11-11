from Crypto.Util.number import *
from secret import flag

p = getPrime(512)
q = getPrime(512)
r = getPrime(512)

m = bytes_to_long(flag)

e = 65537

c = pow(m, e, p*q*r)

print(f'n = {p*q*r}')
print(f'pq = {p*q}')
print(f'c = {c}')
