from Crypto.Util.number import *

def nextPrime(n):
    while True:
        n += (n % 2) + 1
        if isPrime(n):
            return n

with open('g.enc','rb') as f:
    g_int = bytes_to_long(f.read())

with open('h.enc','rb') as f:
    h_int = bytes_to_long(f.read())

def to_base_5(n):
    res = []
    while n:
        res.append(n%5)
        n//=5
    return res[::-1]

def recover_lengths(glen,hlen):
    fdif = hlen-glen
    for i in range(1,fdif+1):
        if fdif%i==0:
            f = fdif//i
            a = nextPrime(f)
            b = nextPrime(a)
            c = nextPrime(f>>2)
            if a*f+c == glen and b*f+c == hlen:
                return f,a,b,c

g = to_base_5(g_int)
h = to_base_5(h_int)
flen,a,b,c = recover_lengths(len(g),len(h))
print("loaded")
import z3
solver = z3.Solver()
F = [z3.Int(f'f_{i}') for i in range(flen-1)]
for i in F:
    solver.add(z3.Or(i==0,i==1))

F.insert(0,0)
for i in range(len(F)-1): F[i]+=F[i+1]
G, H = [[_ for i in range(x) for _ in F] for x in [a, b]]
for _ in [G, H]:
    for __ in range(c): _.insert(0, 0)
    for i in range(len(_) -  c): _[i] += _[i+c]

for i,j in zip(g,G):
    solver.add(i==j)

for i,j in zip(h,H):
    solver.add(i==j)

if solver.check()==z3.sat:
    m = solver.model()
    sol = {str(i):m[i].as_long() for i in m}
    sol = [sol[f'f_{i}'] for i in range(len(F)-1)]
    flag= "".join(map(str,sol))
    print(long_to_bytes(int(flag,2)))

#CCTF{_how_finD_7h1s_1z_s3cr3T?!}


