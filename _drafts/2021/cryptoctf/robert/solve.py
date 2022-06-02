from sympy import isprime, divisors, totient, lcm
import sympy
from collections import defaultdict, Counter
from tqdm import tqdm
from math import prod
from functools import lru_cache
import sys
sys.setrecursionlimit(100000)

@lru_cache(None)
def factorint(n):
    return sympy.factorint(n)

CACHE_LIMIT = 10**3

totient_lookup = defaultdict(set)
lambda_lookup = defaultdict(list)

def tot_lam_facs(fac_dict):
    res = []
    for prime,power in fac_dict.items():
        res.append( (prime-1)*pow(prime, power-1))
    return prod(res), lcm(res)

for i in tqdm(range(1,CACHE_LIMIT),desc = 'precomputation'):
    factors = factorint(i)
    tot,lam = tot_lam_facs(factors)
    totient_lookup[tot].add(i)
    lambda_lookup[lam].append(i)


def calc_inv_tot(n):
    print(n)
    if totient_lookup[n]:
        for i in lambda_lookup[n]:
            yield i
    # elif n<CACHE_LIMIT:
    #     yield from []
    #     return

    dd = [d for d in divisors(n) if isprime(d+1)]
    can_repeat = {p for p in dd if n%(p*p)==0}
    for f in dd[1::-1]:
        print("f=",f)
        phim = n//(f-1)
        if f==2:
            yield from []
            return
        for m in calc_inv_tot(phim):
            if any(v>1 and i not in can_repeat for i,v in factorint(m).items()):
                continue
            res = f*m
            facs_res = factorint(f*m)
            lam_res, tot_res = tot_lam_facs(facs_res)
            if tot_res == n:
                totient_lookup[n].add(res)
                yield res


def phie(m):
    facs = factorint(m)
    phis = [(m//((q-1)*pow(q,i)),q,i) for q,f in facs.items() for i in range(1,f+1) ]
    phis = [i for i in phis if i[0]%2==0 or i[0]==1]
    print(phis)
    for phii, q,f in phis:
        for kij in phie(phii):
            if gcd(kij,q)==1:
                yield kij*pow(q,f+1)



