from z3 import *

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

def check(input):
    v4=1
    v5=0
    for i in range(9):
         v4=(ord(input[i])+v4)&0xffff
         v5=(v4+v5)&0xffff
    if v4^v5==0x12e1:
         print("good job!")


input = [BitVec(f'input_{i}',16) for i in range(9)]
v4 = 1
v5 = 0
for i in range(9):
    v4 = input[i]+v4
    v5 = v4+v5

solver = Solver()
solver.add(v4^v5 == 0x12e1)
for inp in input:
    solver.add(Or(inp == ord("_"),And(inp>=ord("a"),inp<=ord("z"))))

for m in all_smt(solver, input):
    print(bytes(m.eval(i).as_long() for i in input))
