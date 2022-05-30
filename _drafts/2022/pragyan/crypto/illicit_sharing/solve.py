from Crypto.Util.number import *
from sympy import nextprime
from gmpy2 import iroot
import statistics
from tqdm import tqdm

def get_diffs(bits,n=100):
    diffs = []
    for _ in tqdm(range(n)):
        p0 = getPrime(bits)
        p1 = nextprime(p0)
        diffs.append(p1-p0)
    return diffs

def factor(n0,n1,x,y):
    b = n1-n0-x*y
    d2 = (b*b-4*n0*x*y)
    d,isper = iroot(d2,2)
    if not isper:
        return 
    p,q = (b+d)//(2*x), (b-d)//(2*x)
    if n0%q == 0:
        return n0//q,q
    elif n0%p == 0:
        return p, n0//p
    
def try_dec(n0,n1,ul=5000):
    for x in range(2,ul,2):
        for y in range(2,x,2):
            pq = factor(n0,n1,x,y)
            if pq:
                return pq

p0,q0 = getPrime(1024),getPrime(255)
p1,q1 = nextprime(p0), nextprime(q0)
n0,n1 = p0*q0, p1*q1
x,y = p1-p0, q1-q0
