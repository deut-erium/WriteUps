from pwn import remote
import gmpy2
from functools import reduce
HOST, PORT = "185.172.165.118", 4008

REM = remote(HOST,PORT)

REM.recvuntil(b'>')

def gcd(*args):
    return reduce(gmpy2.gcd,args)

def gen_new():
    REM.sendline(b'1')
    data = REM.recvuntil(b'>')
    seed = int(data.strip().split()[0])
    return seed

seeds = []
for i in range(10):
    print(i)
    seeds.append(gen_new())

diffs = [j-i for i,j in zip(seeds,seeds[1:])]
diffs2 = [b**2 - a*c  for a,b,c in zip(diffs,diffs[1:],diffs[2:]) ]
p = gcd(*diffs2)
a = (diffs[1]*gmpy2.invert(diffs[0],p))%p
b = (seeds[1]-a*seeds[0])%p

assert all(j == (a*i+b)%p for i,j in zip(seeds,seeds[1:]))
print("P:",p)
print("a:",a)
print("b:",b)

next = (a*seeds[-1]+b)%p
print("next",next)
REM.sendline(b'2')
REM.sendline(str(int(next)).encode())

REM.interactive()
