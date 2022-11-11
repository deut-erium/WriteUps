from sage.all import *
from pwn import remote
from functools import reduce

def find_root_temp(n, x):
    low = 0
    high = n
    while low < high:
        mid = (low+high)//2
        if mid**x < n:
            low = mid+1
        else:
            high = mid
    return low

def crack_unknown_increment(states, modulus, multiplier):
    increment = (states[1] - states[0]*multiplier) % modulus
    return modulus, multiplier, increment

def crack_unknown_multiplier(states, modulus):
    multiplier = (states[2] - states[1]) * inverse_mod(states[1] - states[0], modulus) % modulus
    return crack_unknown_increment(states, modulus, multiplier)

def crack_unknown_modulus(states):
    diffs = [s1 - s0 for s0, s1 in zip(states, states[1:])]
    zeroes = [t2*t0 - t1*t1 for t0, t1, t2 in zip(diffs, diffs[1:], diffs[2:])]
    modulus = abs(reduce(gcd, zeroes))
    return crack_unknown_multiplier(states, modulus)

r = remote('chall.nitdgplug.org', 30205, level='debug')

N = int(r.recvline().split()[-1])
e = 3

r.recvuntil(b'$ ')
s = []

for i in range(9):
    r.sendline('1')
    s.append(int(r.recvline().split()[-1]))
    r.recvuntil('$ ')

mod, mul, inc  = crack_unknown_modulus(s)
next_num = (s[-1]*mul + inc)%mod

r.sendline('1')
s.append(int(r.recvline().split()[-1]))
assert s[-1] == next_num
r.recvuntil('$ ')

next_num = (s[-1]*mul + inc)%mod
next_num2 = (next_num*mul + inc)%mod

r.sendline('2')
c1 = int(r.recvline().split()[-1])
r.recvuntil('$ ')
r.sendline('2')
c2 = int(r.recvline().split()[-1])
r.recvuntil('$ ')

def _polynomial_gcd(a, b):
    assert a.base_ring() == b.base_ring()
    while b:
        try:
            a, b = b, a % b
        except RuntimeError:
            raise ArithmeticError("b is not invertible", b)
    return a

x = Zmod(N)['X'].gen()
poly1 = (x+next_num)**3-c1
poly2 = (x+next_num2)**3-c2
g = -_polynomial_gcd(poly1,poly2).monic()

print( bytes.fromhex(hex(int(g[0]))[2:]))

