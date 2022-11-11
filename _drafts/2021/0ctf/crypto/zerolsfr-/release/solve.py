#!/usr/bin/env python3
from z3 import *
import time
from functools import reduce
from hashlib import sha256
from itertools import product
import string
import pwn

POW_CHARSET = (string.ascii_letters+ string.digits + '!#$%&*-?').encode()


def _prod(L):
    return And(L)

def _sum(L):
    return reduce(Xor,L)

def n2l(x, l):
    return list(map(int, '{{0:0{}b}}'.format(l).format(x)))

class Generator1:
    def __init__(self, key: list):
        assert len(key) == 64
        self.NFSR = key[: 48]
        self.LFSR = key[48: ]
        self.TAP = [0, 1, 12, 15]
        self.TAP2 = [[2], [5], [9], [15], [22], [26], [39], [26, 30], [5, 9], [15, 22, 26], [15, 22, 39], [9, 22, 26, 39]]
        self.h_IN = [2, 4, 7, 15, 27]
        self.h_OUT = [[1], [3], [0, 3], [0, 1, 2], [0, 2, 3], [0, 2, 4], [0, 1, 2, 4]]

    def g(self):
        x = self.NFSR
        return _sum(_prod([x[i] for i in j]) for j in self.TAP2)

    def h(self):
        x = [self.LFSR[i] for i in self.h_IN[:-1]] + [self.NFSR[self.h_IN[-1]]]
        return _sum(_prod([x[i] for i in j]) for j in self.h_OUT)

    def f(self):
        return _sum([self.NFSR[0], self.h()])

    def clock(self):
        o = self.f()
        self.NFSR = self.NFSR[1: ] + [_sum([self.LFSR[0] , self.g()])] 
        self.LFSR = self.LFSR[1: ] + [_sum(self.LFSR[i] for i in self.TAP)]
        return o

class Generator2:
    def __init__(self, key):
        assert len(key) == 64
        self.NFSR = key[: 16]
        self.LFSR = key[16: ]
        self.TAP = [0, 35]
        self.f_IN = [0, 10, 20, 30, 40, 47]
        self.f_OUT = [[0, 1, 2, 3], [0, 1, 2, 4, 5], [0, 1, 2, 5], [0, 1, 2], [0, 1, 3, 4, 5], [0, 1, 3, 5], [0, 1, 3], [0, 1, 4], [0, 1, 5], [0, 2, 3, 4, 5], [
            0, 2, 3], [0, 3, 5], [1, 2, 3, 4, 5], [1, 2, 3, 4], [1, 2, 3, 5], [1, 2], [1, 3, 5], [1, 3], [1, 4], [1], [2, 4, 5], [2, 4], [2], [3, 4], [4, 5], [4], [5]]
        self.TAP2 = [[0, 3, 7], [1, 11, 13, 15], [2, 9]]
        self.h_IN = [0, 2, 4, 6, 8, 13, 14]
        self.h_OUT = [[0, 1, 2, 3, 4, 5], [0, 1, 2, 4, 6], [1, 3, 4]]

    def f(self):
        x = [self.LFSR[i] for i in self.f_IN]
        return _sum(_prod([x[i] for i in j]) for j in self.f_OUT)
 
    def h(self):
        x = [self.NFSR[i] for i in self.h_IN]
        return _sum(_prod([x[i] for i in j]) for j in self.h_OUT)        

    def g(self):
        x = self.NFSR
        return _sum(_prod([x[i] for i in j]) for j in self.TAP2)  

    def clock(self):
        self.LFSR = self.LFSR[1: ] + [_sum(self.LFSR[i] for i in self.TAP)]
        self.NFSR = self.NFSR[1: ] + [_sum([self.LFSR[1] , self.g()])]
        return _sum([self.f() , self.h()])



class Generator3:
    def __init__(self,key):
        self.LFSR = key 
        self.TAP = [0, 55]
        self.f_IN = [0, 8, 16, 24, 32, 40, 63]
        self.f_OUT = [[1], [6], [0, 1, 2, 3, 4, 5], [0, 1, 2, 4, 6]]

    def f(self):
        x = [self.LFSR[i] for i in self.f_IN]
        return _sum(_prod([x[i] for i in j]) for j in self.f_OUT)

    def clock(self):
        self.LFSR = self.LFSR[1: ] + [_sum(self.LFSR[i] for i in self.TAP)]
        return self.f()

def solve_pow(chall,hash_out):
    for comb in product(POW_CHARSET,repeat=4):
        if sha256(bytes(comb)+chall).hexdigest()==hash_out:
            return bytes(comb)

def all_smt(s, initial_terms):
    def block_term(s, m, t):
        s.add(t != m.eval(t))
    def fix_term(s, m, t):
        s.add(t == m.eval(t))
    def all_smt_rec(terms):
        if sat == s.check():
           m = s.model()
           yield m
           for i in range(len(terms)):
               s.push()
               block_term(s, m, terms[i])
               for j in range(i):
                   fix_term(s, m, terms[j])
               for m in all_smt_rec(terms[i:]):
                   yield m
               s.pop()   
    for m in all_smt_rec(list(initial_terms)):
        yield m   

HOST, PORT = 'localhost', 31337
HOST = '111.186.59.28'

def solve():
    REM = pwn.remote(HOST, PORT)
    pow_chall = REM.recvline()


    REM.recvline()
    pow_chall,pow_hash = pwn.re.search(b'\+ (.*)\) == ([0-9a-f]{64})',pow_chall).groups()
    REM.sendline(solve_pow(pow_chall,pow_hash.decode()))
    start = time.time()
    REM.recvline()
    REM.sendline('1')
    keystream = b''
    for _ in range(5):
        ks=REM.recvuntil(b':::end')
        keystream += pwn.re.search(b'start:::(.|\s){1000}:::end',ks)[0][8:-6]

    bitstream = n2l(int.from_bytes(keystream,'big'),len(keystream)*8)
    hint_hash = REM.recvuntil(b'k:')
    hint_hash = pwn.re.search(b'([0-9a-f]{64})',hint_hash)[1].decode()

    key = [Bool(str(i)) for i in range(64)]
    g = Generator1(key)
    solver = Solver()

    for i in range(56):
        for _ in range(1):
            o = g.clock()
        solver.add(o==bool(bitstream[i]))

    for m in all_smt(solver,key):
        t = time.time()-start
        print(t)
        if t>50:
            return 0
        bs = [bool(m[i]) for i in key]
        bsbin = "".join(map(lambda x:str(int(x)),bs))
        bsint = int(bsbin,2)
        if sha256(str(bsint).encode()).hexdigest()==hint_hash:
            REM.sendline(str(bsint))
            break

    REM.recvline()
    REM.recvline()
    REM.sendline('3')
    keystream = b''
    for _ in range(5):
        ks=REM.recvuntil(b':::end')
        keystream += pwn.re.search(b'start:::(.|\s){1000}:::end',ks)[0][8:-6]

    bitstream = n2l(int.from_bytes(keystream,'big'),len(keystream)*8)
    hint_hash = REM.recvuntil(b'k:')
    hint_hash = pwn.re.search(b'([0-9a-f]{64})',hint_hash)[1].decode()

    key = [Bool(str(i)) for i in range(64)]
    g = Generator3(key)
    solver = Solver()

    for i in range(128):
        for _ in range(3):
            o = g.clock()
        solver.add(o==bool(bitstream[i]))
    counter=0

    for m in all_smt(solver,key):
        t = time.time()-start
        print(t)
        if t>50:
            return 0
        counter+=1
        bs = [bool(m[i]) for i in key]
        bsbin = "".join(map(lambda x:str(int(x)),bs))
        bsint = int(bsbin,2)
        if sha256(str(bsint).encode()).hexdigest()==hint_hash:
            print('broken harts braaa')
            REM.sendline(str(bsint))
            break
    
    print(counter, time.time()-start)
    try:
        REM.interactive()
    except EOFError:
        return 0

while True:
    r = solve()
    if r:
        break

#flag{we_have_tried_our_best_to_prevent_the_use_of_z3}
