# from z3 import *
from cvc5.pythonic import *
with open('chall.txt','r') as f:
    data = f.read().strip().split('\n')

flag_chunks = [int(i.split(': ')[1]) for i in data[:4]]
states = list(map(int,data[4:]))


vec = [BitVec(f'x_{i}',64) for i in range(607)]

tap = 0
feed = 607 - 273

def uint64():
    global tap
    global feed
    global vec
    tap-=1
    if tap <0:
        tap += 607
    feed-=1
    if feed <0:
        feed += 607
    x = simplify(vec[feed] + vec[tap])
    vec[feed] = x
    return x

flag_xored = []
for i in range(4):
    flag_xored.append(uint64())


solver = Solver()
gap = 0
for i in range(607):
    solver.add(states[i]==uint64())
    j = 0
    while j<gap:
        uint64()
        j+=1
    gap = (gap+1)%13
    # print(i,solver.check())
if solver.check()==sat:
    ff = [(flag_chunks[i]^m.eval(flag_xored[i]).as_long()) for i in range(4)]
    print(b''.join([bytes.fromhex(hex(i)[2:])[::-1] for i in ff]))

# b'actf{i_c4n_f0rs33_th3_p4s7_t00_}'
# https://cs.opensource.google/go/go/+/refs/tags/go1.18.1:src/math/rand/rng.go;drc=e7c56fe9948449a3710b36c22c02d57c215d1c10;bpv=0;bpt=1;l=182
