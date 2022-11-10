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

array = BoolVector('array',14*14)

def exactly_n_true(vars,n ):
    return PbEq([(i,1) for i in vars], n)

def neighbours(x,y):
    adj_block = [(i,j) for i in range(14) for j in range(14) if abs(x-i)<=1 and abs(y-j)<=1]
    adj_block.remove((x,y))
    return adj_block

solver = Solver()
for i in range(14):
    # exactly 3 true in each row
    solver.add(exactly_n_true(array[14*i:14*i+14],3))
    # exactly 3 true in each column
    solver.add(exactly_n_true([ array[14*j+i] for j in range(14)],3))

for i in range(14):
    for j in range(14):
        for p,q in neighbours(i,j):
            solver.add(Implies(array[14*i+j],Not(array[14*p+q])))

CHAR_MATRIX = """aaaaabbbbcccdd
aaaaabbbbccccd
aaeaaabbbccccd
aaefaabbbcccgd
eeefffffbccggd
feeffffggggggd
fffffffhhhgggd
ffffhhhhhhgggd
ffijjjjhkkllmd
iiijjkkkkkllmm
iijjjkkkklllmm
iijjjkkkklllmm
ijjjjjkknnllmm
ijjjjnnnnnllll"""
CHAR_MATRIX = "".join(CHAR_MATRIX.split())
matrix_groups = [ [i for i in range(14*14) if CHAR_MATRIX[i]==character] for character in "abcdefghijklmn"]

for m in matrix_groups:
    solver.add(exactly_n_true([array[i] for i in m],3))

# if solver.check()==sat:
for model in all_smt(solver,array):
    model = solver.model()
    solution = [bool(model.eval(i)) for i in array]
    sol = "".join(map(lambda x:str(int(x)),solution))
    print("\n".join(sol[i:i+14] for i in range(0,14*14,14)))


