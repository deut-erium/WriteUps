CHARSET = b'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_'
from itertools import product
class ENC:
    def __init__(self):
        self.state = [0 for i in range(242)]
        self.ini = 0

    def transform(self,b):
        for i in range(23):
            v4 = self.state[self.ini]
            self.state[self.ini] = b ^ v4
            if b > v4:
                self.ini += 11
            else:
                self.ini += 10
            if (i & 1) == 0:
                v3 = self.ini - 11 + 21 * (i / -2)
                if v3 == -1:
                    self.ini += 10
                if v3 == 10:
                    self.ini -= 10
            self.ini %= 242
            b ^= v4
        return b

    def encrypt(self,text):
        ct = bytearray()
        for b in text:
            ct.append(self.transform(b))
        return ct


def encrypt(text):
    cyph = ""
    for i in range(len(text)):
        cyph += chr(transform(ord(text[i])))
    return cyph


with open('flag.enc','rb') as f:
    ct = f.read()

head = b'_9j_4AAQSkZF+*v='

repeatlen=2
start=11
for p in product(range(256),repeat=repeatlen):
    if ENC().encrypt(b'_9j_4AAQSkZ'+bytes(p))[start:start+repeatlen] == ct[start:start+repeatlen]:
        print(p)

encs = [ENC().encrypt(head[:10]+bytes([90,11,52,124])+bytes([i]))[14] for i in range(256)]




# pt = bytearray(ct[:10])
# for i in range(10,20):
#     candidates_last = [61,90,98]
#     candidates = []
#     for c in candidates_last:
#         for j in range(256):
#             if ENC().encrypt(pt+bytes([c,j]))[i+1]==ct[i+1]:
#                 candidates.append(j)
#     print(candidates)


# from z3 import *
# STATE = Array('STATE', BitVecSort(8), BitVecSort(8))

# for i in range(248):
#     STATE = Store(STATE, i, 0)

# # STATE = [BitVec(f'STATE_{i}',8) for i in range(242)]
# IND = BitVec('INDEX',8)

# INPUT = [BitVec(f'INPUT_{i}',8) for i in range(256)]

# def TRANSFORM(byte):
#     global STATE
#     global IND
#     for i in range(23):
#         v4 = STATE[IND]
#         STATE = Store(STATE, IND, v4^byte)
#         IND = If( UGT(byte, v4), IND+11, IND+10)
#         if (i&1)==0:
#             v3 = IND - 11 + 21*(i//-2)
#             IND = If( v3==-1, IND+10, IND)
#             IND = If( v3==10, IND-10, IND)
#         IND = URem(IND, 242)
#     return byte^v4

# encrypted = encrypt('asdfasdfasdfasdf').encode()

# S = Solver()

# for a,b in zip(INPUT,encrypted):
#     S.add(TRANSFORM(a)==b)




