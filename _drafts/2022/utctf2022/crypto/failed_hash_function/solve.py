from z3 import *
from pwn import remote

HOST, PORT = "misc1.utctf.live",5000
REM = remote(HOST, PORT)

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
               yield from all_smt_rec(terms[i:])
               s.pop()   
    yield from all_smt_rec(list(initial_terms))  

def trailing(x):
    a = 0
    for _ in range(15):
        if x & 1:
            break
        x >>= 1
        a += 1
    return a

def hash(s,k1,k2):
    output = ''
    for x in s:
        for y in s:
            output+=hex(trailing((k1 ^ x) * (k2 ^ y)))[2:]
    return output

def solve(s1,s2,hashs1,hashs2):
    k1 = BitVec('k1',16)
    k2 = BitVec('k2',16)
    solver = Solver()
    solver.add(Extract(15,8,k1)==0)
    solver.add(Extract(15,8,k2)==0)

    def hash_constraints(s,hash_str):
        i = 0
        constraints = []
        for x in s:
            for y in s:
                num_zeros = int(hash_str[i],16)
                mask = 2**(num_zeros) - 1
                mul = (k1^x)*(k2^y)
                constraints.append(mul&mask == 0)
                constraints.append( Extract(num_zeros,num_zeros,mul)==1)
                i+=1
        return constraints
    solver.add(hash_constraints(s1,hashs1))
    solver.add(hash_constraints(s2,hashs2))
    for m in all_smt(solver,[k1,k2]):
        yield [m[i].as_long() for i in m.decls()]
        
def num_sol(s1,s2,k1,k2):
    sols = list(solve(s1,s2,hash(s1,k1,k2),hash(s2,k1,k2)))
    sols = {tuple(sorted(i)) for i in sols}
    print(len(sols))
    return sols





