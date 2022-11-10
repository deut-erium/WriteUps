
#!/usr/bin/env python3
from z3 import *
from pwn import remote
from itertools import permutations


def bytes_to_words(B):
    return [int.from_bytes(B[i:i+4], 'little') for i in range(0, len(B), 4)]

class faulty_arx:
    def __init__(self, key,nonce:list):
        self.ROUNDS = 20
        self.counter = 0
        self.f = 0
        self.key = key
        self.nonce = nonce

    def _init_state(self, key, nonce, counter):
        state = bytes_to_words(b'downunderctf2022')
        state = [BitVecVal(i,32) for i in state]
        state += key
        state += [BitVecVal(counter,32)] + [BitVecVal(i,32) for i in bytes_to_words(nonce)]
        return state

    def _QR(self, S, a, b, c, d):
        S[a] = (S[a] + S[b]) ; S[d] ^= S[a]; S[d] = RotateLeft(S[d], 16)
        S[c] = (S[c] + S[d]) ; S[b] ^= S[c]; S[b] = RotateLeft(S[b], 12 ^ self.f)
        S[a] = (S[a] + S[b]) ; S[d] ^= S[a]; S[d] = RotateLeft(S[d], 8)
        S[c] = (S[c] + S[d]) ; S[b] ^= S[c]; S[b] = RotateLeft(S[b], 7)

    def block(self,inp_x):
        initial_state = self._init_state(self.key, self.nonce, self.counter)
        state = initial_state[:]
        for r in range(0, self.ROUNDS, 2):
            self._QR(state, 0, 4, 8, 12)
            self._QR(state, 1, 5, 9, 13)
            self._QR(state, 2, 6, 10, 14)
            self._QR(state, 3, 7, 11, 15)

            x = 0
            if r == self.ROUNDS - 2:
                x = inp_x

            if x == 1:
                self.f = 1
            self._QR(state, 0, 5, 10, 15)
            self.f = 0

            if x == 2:
                self.f = 1
            self._QR(state, 1, 6, 11, 12)
            self.f = 0

            if x == 3:
                self.f = 1
            self._QR(state, 2, 7, 8, 13)
            self.f = 0

            if x == 4:
                self.f = 1
            self._QR(state, 3, 4, 9, 14)
            self.f = 0

        out = [(i + s)  for i, s in zip(initial_state, state)]
        self.counter += 1
        print(self.counter)
        return out

    def stream(self, length,inp_x):
        out = []
        while length > 0:
            block = self.block(inp_x)
            t = min(length, len(block))
            out += block[:t//4]
            length -= t
        return out

HOST, PORT =  "2022.ductf.dev",30007
REM = remote(HOST, PORT)

key_constraints = []
key = [z3.BitVec(f'k_{i}',32) for i in range(8)]

key = [z3.BitVec(f'k_{i}',8) for i in range(32)]
for i in range(32):
    key_constraints.append(Or(And(key[i]>=48,key[i]<=57),And(key[i]>=97,key[i]<=102)))
key = [Concat(key[i:i+4]) for i in range(0,32,4)]


nonce = bytes.fromhex(REM.recvline().strip().decode())
cts = []
for _ in range(5):
    cts.append(bytes.fromhex(REM.recvline().strip().decode()))

streams = []
for i in range(5):
    f = faulty_arx(key, nonce)
    streams.append(f.block(i))

cts = [bytes_to_words(i) for i in cts]
for item,p in enumerate(permutations(cts)):
    solver = Solver()
    solver.add(key_constraints)
    for i in range(5):
        for a,b,_ in zip(p[i],streams[i],range(4)):
            solver.add(a==b)
    if solver.check()==sat:
        model = solver.model()
        break
    else:
        print("none",item)


