from Crypto.Util.number import *
from secret import flag
pt=bytes_to_long(flag)
p,q,r=[getPrime(1024) for _ in [1,1,1]]
n=p*q*r
e=65537
x=(getPrime(77)*p+n)%(q*r)
ct=pow(pt,e,n)
print(f"{ct=}\n{n=}\n{x=}")
