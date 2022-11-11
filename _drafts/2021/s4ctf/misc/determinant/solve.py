import pwn
import re
from gmpy2 import gcdext
from sympy import factorint
from collections import Counter
from z3 import *

pwn.context(log_level=0)
HOST, PORT = "157.90.231.113", 2570

REM = pwn.remote(HOST, PORT)

def get_chall(REM):
    chall = REM.recvregex(b'greater than \d+\n')
    matrix = eval(re.search(b'\[\[.*\]\]',chall)[0])
    bound = eval(re.search(b'(\d+)\n',chall)[1])
    return matrix, bound

def get_symbols(matrix):
    symbols = []
    n = len(matrix)
    for i in range(n):
        for j in range(n):
            elem = matrix[i][j]
            if isinstance(elem,(str)):
                symbols.append(Int(elem))
                matrix[i][j] = symbols[-1]
    return matrix,symbols

def solve_bv(matrix,limit):
    bv_size = (limit.bit_length()+2)*3
    symbols = []
    n = len(matrix)
    constraints = []
    for i in range(n):
        for j in range(n):
            elem = matrix[i][j]
            if isinstance(elem,(str)):
                symbols.append(BitVec(elem,bv_size))
                matrix[i][j] = symbols[-1]
                if len(symbols)>=2 and limit>2**16:
                    constraints.append(symbols[-1]==limit+1)
            else:
                matrix[i][j] = BitVecVal(elem,bv_size)

    constraints.append(BVMulNoOverflow(matrix[0][0],matrix[1][1],False))
    constraints.append(BVMulNoOverflow(matrix[0][1],matrix[1][0],False))
    constraints.append(BVSubNoOverflow(matrix[0][0]*matrix[1][1],matrix[0][1]*matrix[1][0] ))
    for i in symbols:
        constraints.append(i>limit)
    constraints.append(matrix[0][0]*matrix[1][1]-matrix[0][1]*matrix[1][0]==1)
    s = Solver()
    s.add(constraints)
    if s.check()==sat:
        m = s.model()
        return [m.eval(i).as_long() for i in symbols]

def determinant(matrix):
    if len(matrix)==2:
        return matrix[0][0]*matrix[1][1]-matrix[0][1]*matrix[1][0]
    n = len(matrix)
    result = 0
    for const in range(n):
        print([(i,(i-const)%n) for i in range(n) ])
        print([(i,(const-i)%n) for i in range(n) ])
        result+=Product([ matrix[i][(i-const)%n] for i in range(n)])
        result-=Product([ matrix[i][(const-i)%n] for i in range(n)])
    return result

def solve(matrix,bound):
    mat,sym = get_symbols(matrix)
    s = Solver()
    for i in sym:
        s.add(i>bound)
    s.add(determinant(mat)==1)
    if s.check()==sat:
        m = s.model()
        return [m.eval(i).as_long() for i in sym]


def biggest_facs(n):
    a,b=1,1
    for i,v in enumerate(Counter(factorint(n)).elements()):
        if i&1:
            a*=v
        else:
            b*=v
    return a,b

def istr(x):
    return isinstance(x,str)


def solve_single(vals):
    a,b,c,d = vals
    if istr(a):
        return [(b*c+1)//d]
    if istr(b):
        return [(a*d-1)//c]
    if istr(c):
        return [(a*d-1)//b]
    if istr(d):
        return [(b*c+1)//a]

#ad-bc=1

def solve_double(vals):
    a,b,c,d = vals
    if istr(a) and istr(b):
        _, v1,v2 = gcdext(d,-c)
        return int(v1),int(v2)
    if istr(a) and istr(c):
        _, v1,v2 = gcdext(d,-b)
        return int(v1),int(v2)
    if istr(d) and istr(b):
        _, v1,v2 = gcdext(a,-c)
        return int(v2),int(v1)
    if istr(c) and istr(d):
        _, v1,v2 = gcdext(a,-b)
        return int(v2),int(v1)
    if istr(a) and istr(d):
        return biggest_facs(b*c+1)
    if istr(b) and istr(c):
        return biggest_facs(a*d-1)
    
def solve_gcd(matrix,bound):
    (a,b),(c,d) = matrix[0],matrix[1]
    vals = [a,b,c,d]
    c = sum(istr(i) for i in vals)
    print(c,vals)
    if c==1:
        return solve_single(vals)
    elif c==2:
        return solve_double(vals)
    else:
        return solve_bv(matrix,bound)


while True:
    mat,limit = get_chall(REM)
    sols = ",".join(map(str,solve_bv(mat,limit)))
    REM.sendline(sols)

#from z3 import *
#a,b,c,d,e,f,g,h,i = Ints('a b c d e f g h i')
#mat = [[a,b,c],[d,e,f],[g,h,i]]
#(10^77p + q)(10^77q+p)



