from parameter import *
from gmpy2 import isqrt
from math import gcd
e = 1
for fac in publickey_factors:
    e *= fac

def cf_expansion(n, d):
    e = []
    q = n // d
    r = n % d
    e.append(q)
    while r != 0:
        n, d = d, r
        q = n // d
        r = n % d
        e.append(q)
    return e

def convergents(e):
    n = [] # Nominators
    d = [] # Denominators
    for i in range(len(e)):
        if i == 0:
            ni = e[i]
            di = 1
        elif i == 1:
            ni = e[i]*e[i-1] + 1
            di = e[i]
        else: # i > 1
            ni = e[i]*n[i-1] + n[i-2]
            di = e[i]*d[i-1] + d[i-2]
        n.append(ni)
        d.append(di)
        yield (ni, di)

for pk,pd in convergents(cf_expansion(n,e)):
    print(pk/pd)
    phii = (e*pd -1)//pk
    b = n+1-phii
    p = (b - isqrt(b**2 - 4*n))//2
    if gcd(n,p)!=1:
        q = n//p
        d = pow(e,-1,(p-1)*(q-1))
        m = pow(c,d,n)
        print( m.to_bytes( (m.bit_length()+7)//8,'big'))
        break


