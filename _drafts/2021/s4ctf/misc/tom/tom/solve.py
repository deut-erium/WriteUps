import pwn
import re
from sympy import factorint, nextprime,root,primerange
from collections import Counter
from itertools import product


HOST, PORT = "157.90.231.113",7027
#REM = pwn.remote(HOST, PORT)

def f_list(n):
    return list(Counter(factorint(n)).elements())

def tom(n):
    c = (n%2)^1
    while True:
        FU = list(f_list(n+c))
        FD = list(f_list(n-c))
        if len(FU)==2:
            return c,FU
        elif len(FD)==2:
            return c,FD
        else:
            c+=2

def get_chall(REM):
    chall = REM.recvregex(b'tom\(n\) = \d+\n')
    match = re.search(b'than (\d+).* than (\d+).* = (\d+)',chall)
    return list(map(int,match.groups()))

def try_find(low,hi,order):
    startp = nextprime(2*low)
    nextp = nextprime(startp)
    while nextp-startp<=2*order:
        startp,nextp = nextp, nextprime(startp)
    return (startp+nextp)//2

def try_find2(low,hi,order,ext=400):
    for jjj in range(1,2):
        mid = int(root(low*jjj,2))
        lowest,highest = max((mid-ext)**2,low), min(hi,(mid+ext)**2)
        print(lowest,highest)
        vals = [i*j for i,j in product(primerange(mid-ext,mid+ext),repeat=2)]
        for small_p in primerange(0,400):
            vals.extend([i*small_p for i in primerange(lowest//small_p,highest//small_p)])
        vals = sorted(set(vals))
        for i in range(len(vals)-1):
            if vals[i+1]-vals[i]>=2*order:
                print(vals[i],vals[i+1])
    

