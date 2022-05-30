from itertools import product
from sympy import isprime
from tqdm import tqdm

def check_2(num):
    nums = str(num)
    return num == sum(int(i)**len(nums) for i in nums)


template = '0x199{}465f'
for pos in tqdm(product('0123456789abcdef',repeat=5),total=16**5):
    num = int(template.format(''.join(pos)),16)
    if isprime(num) and check_2(num):
        print(num,pos)

"""
  if ( *a1 != 0x53 )
    return 0LL;
  if ( (*a1 ^ a1[15]) != 7 )
    return 0LL;
  if ( (a1[4] & a1[7]) != a1[7] && (a1[4] & a1[7]) != a1[4] )
    return 0LL;
  if ( ((a1[7] ^ *a1) & 0xF) != 0 )
    return 0LL;
  if ( (a1[4] & 0xF0) != 0 && (char)a1[4] < 0 )
    return 0LL;
  if ( (a1[4] ^ a1[6]) != 8 )
    return 0LL;
  if ( (char)a1[6] - (char)a1[3] != 3 )
    return 0LL;
  if ( (char)a1[11] >> 1 != a1[8] )
    return 0LL;
  if ( a1[11] != 102 )
    return 0LL;
  if ( (char)a1[10] >> 3 != 15 && ((a1[10] ^ a1[3]) & 7) != 0 )
    return 0LL;
  if ( (unsigned __int8)a1[1] * (unsigned __int8)a1[13] != 0x17AB && a1[13] > a1[1] )
    return 0LL;
  if ( a1[14] != 68 )
    return 0LL;
  if ( (a1[12] ^ a1[14]) != 48 )
    return 0LL;
  v3 = (char)a1[2];
  if ( v3 != (unsigned int)toupper('z') )
    return 0LL;
  if ( a1[5] == 'A' )
    return (char)a1[9] - (char)a1[14] == 8;
"""
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

a = [BitVec(f'a{i}',8) for i in range(16)]
s = Solver()
s.add([
    a[0]==83,
    a[0]^a[15]==7,
    a[4] == a[7],
    # a[4]&a[7] == a[7],
    # a[4]&a[7] == a[4],
    (a[7]^a[0])&0xf == 0,
    (a[4] & 0xf0)==0,
    (a[4]^a[6])==8,
    a[6]-a[3] == 3,
    LShR(a[11],1) == a[8],
    a[11]==102,
    LShR(a[10],3)==15,
    (a[10] ^ a[3]) & 7 == 0,
    a[13]==83,
    a[1]==73,
    a[14]==68,
    a[12]^a[14]==48,
    a[2] == ord('Z'),
    a[5] == ord('A'),
    a[9]-a[14] == 8,
    ])

for m in all_smt(s,a):
    # string = bytes([ m[i].as_long() for i in sorted(m.decls(),key=lambda x:int(str(x)[1:]))])
    string = bytes([m[a[i]].as_long() for i in range(16)])
    print(string)

def raw_checks(a):
    if a[0]!=0x53:
        return 0
    if a[0]^a[15]!=7:
        return 1
    if (a[4]&a[7] != a[7]) and (a[4]&a[7]!=a[4]):
        return 2
    if (a[7]^a[0])&0xf !=0:
        return 3
    if (a[4]&0xf0)!=0:
        return 4
    if a[6]-a[3]!=3:
        return 5
    if (a[11]>>1)!=a[8]:
        return 6
    if a[11]!=102:
        return 7
    if (a[10]>>3)!=15 and (a[10]^a[3])&7 !=0:
        return 8
    if a[1]*a[13]!=0x17ab and a[13]>a[1]:
        return 9
    if a[14]!=68:
        return 10
    if a[12]^a[14]!=48:
        return 11
    if a[2]!=ord('Z'):
        return 12
    if a[9]-a[14]!=8:
        return 13
    if a[5]!=ord('A'):
        return 14
    return -1

assert raw_checks(string)==-1

