import pwn
import re
from hashlib import sha256
from math import prod
from itertools import combinations, chain,product
import string

from Crypto.Util.number import inverse
from Crypto.Random import random
from fastecdsa.curve import Curve
from fastecdsa.point import Point

CHARSET = (string.ascii_lowercase + string.ascii_uppercase).encode()

HOST, PORT = "crypto2.q21.ctfsecurinets.com", 13337

p = 0x402969301d0ec23afaf7b6e98c8a6aebb286a58f525ec43b46752bfc466bc435
gx = 0x3aedc2917bdb427d67322a1daf1073df709a1e63ece00b01530511dcb1bae0d4
gy = 0x21cabf9609173616f5f50cb83e6a5673e4ea0facdc00d23572e5269632594f1d
a = 0x2ad2f52f18597706566e62f304ae1fa48e4062ee8b7d5627d6f41ed24dd68b97
b = 0x2c173bd8b2197e923097541427dda65c1c41ed5652cba93c86a7d0658070c707
q = 0x402969301d0ec23afaf7b6e98c8a6aeb2f4b05d0bbb538c027395fa703234883

def all_subsets(lst):
    return chain.from_iterable([ combinations(lst,r) for r in range(1,len(lst)+1) ])



factors_q = [157 , 2963 , 83007641671782083660077631317 , 751563746414044381480884376392818373849137]

possible_orders = list(map(prod, all_subsets(factors_q)))


S256 = Curve("S256", p, a, b, q, gx, gy)
G = Point(gx,gy,curve=S256)




"""
import hashlib
E = EllipticCurve(GF(p),[0,0,0,a,b])
our_gen = E.lift_x(16)
our_ord = 9794528862466737592433017304760374843761727873640191428743304917745878353
G = E(gx,gy)
one = q*G

def gen_order(G):
    for o in possible_orders:
        if o*G == one:
            return o

def ECDLP(point,gen,gen_order=None):
    if not gen_order:
        gen_order = gen.order()
    return discrete_log(point,gen,gen_order,operation='+')

def sign(msg,priv,G,gen_order):
    z = int(hashlib.sha256(msg).hexdigest(), 16)
    k = random.randrange(1,gen_order-1)
    r = int((k*G)[0])%gen_order
    s = (inverse_mod(k,gen_order) * (z + r*priv))%gen_order
    return r,s


def get_private(r,s,msg,E,p,G,gen_order=None):
    z = int(hashlib.sha256(msg).hexdigest(),16)
    P = E.lift_x(GF(p)(r))
    if not gen_order:
        gen_order = G.order()
    try:
        k = ECDLP(P,G,gen_order)
    except ValueError:
        print('bruh ')
        k = ECDLP(-P,G,gen_order)
    sk_inv = (s*inverse_mod(k,gen_order))%gen_order
    d = ((sk_inv-z)*inverse_mod(r,gen_order))%gen_order
    return d
"""


def PoW(prefix):
    for X in product(CHARSET,repeat=6):
        if sha256(prefix+bytes(X)).hexdigest().startswith('000000'):
            return bytes(X)


REM = pwn.remote(HOST,PORT)
#
#
pow_chall = re.search(b'\(([a-zA-Z]+) \+ X\)',REM.recvline())[1]
#
#
REM.sendline(PoW(pow_chall))
REM.interactive()
