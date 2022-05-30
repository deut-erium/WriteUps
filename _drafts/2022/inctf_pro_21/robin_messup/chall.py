from Crypto.Util.number import *
from gmpy2 import next_prime
from sec import flag
pt=bytes_to_long(flag)
def gen(bits,x=4):
    while x%4!=3 and next_prime(x)%4!=3:
        x=getPrime(bits)
    return x,next_prime(x)
p,q=gen(512)
n=int(p*q)
e=2
ct=pow(pt,e,n)
print(f"{ct=}\n{n=}")
