from z3 import *
from task import SusCipher

S = [
    43,  8, 57, 53, 48, 39, 15, 61,
     7, 44, 33,  9, 19, 41,  3, 14,
    42, 51,  6,  2, 49, 28, 55, 31,
     0,  4, 30,  1, 59, 50, 35, 47,
    25, 16, 37, 27, 10, 54, 26, 58,
    62, 13, 18, 22, 21, 24, 12, 20,
    29, 38, 23, 32, 60, 34,  5, 11,
    45, 63, 40, 46, 52, 36, 17, 56
]

P = [
    21,  8, 23,  6,  7, 15,
    22, 13, 19, 16, 25, 28,
    31, 32, 34, 36,  3, 39,
    29, 26, 24,  1, 43, 35,
    45, 12, 47, 17, 14, 11,
    27, 37, 41, 38, 40, 20,
     2,  0,  5,  4, 42, 18,
    44, 30, 46, 33,  9, 10
]

class crack:
    ROUND = 3
    BLOCK_NUM = 8
    def __init__(self):
        self.S = Function('S', BitVecSort(6), BitVecSort(6))
        self.solver = Solver()
        for i,v in enumerate(S):
            self.solver.add(self.S(i)==v)
        self.keys = [[BitVec(f'k_{r}_{i}',6) for i in range(8) ] for r in range(self.ROUND+1)]

    def _divide(self, v):
        l = []
        for _ in range(self.BLOCK_NUM):
            l.append(v&0b111111)
            v >>=6
        return l[::-1]

    def _combine(self, block):
        res = 0
        for v in block:
            res <<=6
            res |= v
        return res

    def _xor(self, a,b):
        return [x^y for x,y in zip(a,b)]

    def _perm(self, block):
        x = Concat(block)
        output = [0]*48
        for i,v in enumerate(P):
            output[v] = Extract(47-i, 47-i, x)
        return [Concat(output[i:i+6]) for i in range(0,48,6)]

    def _sub(self, block):
        return [self.S(simplify(i)) for i in block]

    def enc(self, block):
        block = self._xor(block, self.keys[0])
        for r in range(self.ROUND):
            block = self._sub(block)
            block = self._perm(block)
            block = self._xor(block, self.keys[r+1])
        return block

    def add_sample(self, inp, oup):
        for a,b in zip(self.enc(self._divide(inp)), self._divide(oup)):
            self.solver.add(a==b)

    def get(self):
        if self.solver.check()==sat:
            model = self.solver.model()
            k = [model.eval(i).as_long() for i in self.keys[0]]
            return self._combine(k)

# print("verifying our modelling")
# import random
# for i in range(100):
#     random_key = random.randint(0,2**48-1)
#     sus = SusCipher(random_key)
#     sus_model = crack()
#     sus_model.solver.check()
#     sus_model.keys = [[BitVecVal(i,6) for i in row] for row in sus.subkeys]
#     for j in range(10):
#         inp = random.randint(0,2**48-1)
#         real_out = sus.encrypt(inp)
#         sym_out_chunks = sus_model.enc(sus_model._divide(inp))
#         sym_out = sus_model.solver.model().eval(Concat(sym_out_chunks))
#         assert sym_out.as_long() == real_out
# print("success")

import pwn
HOST, PORT = "suscipher.chal.ctf.acsc.asia", 13579
REM = pwn.remote(HOST, PORT)

REM.sendline(",".join(str((1<<i)) for i in range(48)))
response = list(map(int,REM.recvline()[2:].strip().split(b', ')))
c = crack()
for i,v in enumerate(response):
    c.add_sample(1<<i,v)

key = c.get()
REM.sendline(str(key))
REM.interactive()
