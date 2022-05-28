from nestools.remote import rem
import z3
from chall import PRNG

def sym_xoroshiro128plus(solver, sym_s0, sym_s1, mask, result):
    s0 = sym_s0
    s1 = sym_s1
    sym_r = (sym_s0 + sym_s1)
    
    condition = z3.Bool('c0x%0.16x' % result)
    solver.add(z3.Implies(condition, (sym_r & mask) == result & mask))
    
    s1 ^= s0
    sym_s0 = z3.RotateLeft(s0, 55) ^ s1 ^ (s1 << 14)
    sym_s1 = z3.RotateLeft(s1, 36)
    
    return sym_s0, sym_s1, condition

def find_seed(results_with_masks):
    start_s0, start_s1 = z3.BitVecs('start_s0 start_s1', 64)
    sym_s0 = start_s0
    sym_s1 = start_s1
    solver = z3.Solver()
    conditions = []
    
    for result, mask in results_with_masks:
        sym_s0, sym_s1, condition = sym_xoroshiro128plus(solver, sym_s0, sym_s1, mask, result)
        conditions.append(condition)
    
    if solver.check(conditions) == z3.sat:
        model = solver.model()
        
        return (model[start_s0].as_long(), model[start_s1].as_long())
    
    else:
        return None

io=rem("35.200.245.250", 1337)
n=int(io.rl().strip().split()[-1])
e=int(io.rl().strip().split()[-1])
state=[]
for _ in range(12):
    io.ru(b"$ ")
    io.sl(b"1")
    state.append(int(io.rl().strip().split()[-1]))

x=[(i,0xffffffffffffffff) for i in state[:10]]
seed=find_seed(x)
g=PRNG(seed[0],seed[1])
l=[g.next() for _ in range(12)]
if l==state:
    print("nice")

ct=[]
for _ in range(17):
    io.ru(b"$ ")
    io.sl(b"2")
    ct.append(int(io.rl().strip().split()[-1]))
a=g.next()
b=g.next()
print(f"""
{a=}
{b=}
ct1={ct[0]}
ct2={ct[1]}
{n=}
{e=}
""")