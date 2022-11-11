from Crypto.Util.number import long_to_bytes
from math import factorial
from tqdm import tqdm
import re
import pickle

N = 64
C = 16
B = 296
#inv_gens = [[ x.index(i) for i in range(64) ] for x in gens]
gens = [[63, 62, 40, 42, 34, 32, 61, 22, 27, 28, 23, 10, 29, 45, 5, 19, 16, 24, 46, 33, 17, 14, 8, 47, 18, 44, 25, 26, 53, 38, 21, 52, 15, 1, 31, 0, 59, 36, 56, 6, 37, 41, 58, 51, 54, 11, 2, 50, 55, 4, 12, 39, 35, 13, 43, 3, 30, 7, 9, 48, 57, 60, 20, 49],
        [0, 39, 59, 31, 9, 41, 52, 1, 25, 55, 15, 37, 28, 48, 43, 58, 40, 38, 24, 18, 10, 60, 44, 63, 20, 57, 26, 27, 45, 4, 54, 46, 51, 42, 47, 29, 6, 11, 16, 35, 32, 49, 5, 53, 30, 8, 56, 19, 50, 2, 23, 34, 14, 3, 12, 22, 13, 17, 21, 33, 62, 61, 36, 7],
        [10, 12, 52, 42, 7, 36, 13, 57, 61, 44, 39, 22, 32, 17, 8, 59, 27, 29, 2, 38, 46, 21, 0, 4, 5, 6, 62, 58, 9, 48, 45, 16, 1, 35, 3, 31, 23, 54, 56, 41, 49, 24, 33, 40, 50, 63, 43, 25, 37, 11, 53, 55, 15, 26, 60, 20, 18, 34, 47, 30, 14, 51, 28, 19],
        [6, 58, 45, 55, 14, 37, 32, 8, 4, 53, 13, 16, 47, 0, 23, 19, 49, 10, 30, 52, 3, 21, 27, 60, 48, 12, 9, 11, 50, 39, 56, 40, 25, 46, 51, 43, 54, 24, 15, 17, 35, 29, 20, 33, 26, 18, 42, 1, 41, 31, 62, 57, 63, 28, 5, 34, 59, 61, 22, 38, 36, 7, 44, 2],
        [34, 60, 50, 25, 9, 40, 21, 26, 29, 59, 1, 44, 42, 15, 23, 48, 57, 27, 55, 6, 11, 33, 35, 38, 51, 16, 53, 14, 52, 47, 49, 5, 54, 4, 12, 18, 61, 24, 3, 43, 0, 36, 45, 17, 62, 63, 28, 58, 37, 13, 8, 31, 56, 19, 10, 39, 30, 41, 20, 22, 32, 2, 7, 46],
        [61, 32, 35, 18, 48, 47, 11, 19, 3, 44, 39, 21, 52, 43, 50, 1, 51, 4, 34, 16, 7, 54, 36, 2, 22, 9, 28, 20, 62, 14, 31, 55, 38, 13, 42, 58, 41, 33, 15, 0, 27, 23, 53, 57, 6, 30, 60, 29, 46, 26, 45, 56, 8, 59, 25, 37, 63, 10, 49, 17, 5, 40, 12, 24],
        [61, 57, 0, 32, 37, 30, 7, 28, 14, 17, 21, 27, 18, 58, 40, 33, 54, 13, 2, 42, 35, 44, 53, 29, 55, 8, 20, 59, 48, 52, 51, 16, 46, 11, 39, 24, 36, 4, 41, 31, 60, 43, 62, 10, 6, 34, 56, 47, 38, 45, 23, 63, 26, 49, 1, 3, 12, 19, 5, 25, 15, 22, 9, 50],
        [18, 41, 21, 26, 10, 13, 32, 51, 33, 16, 54, 28, 25, 45, 11, 39, 56, 37, 42, 2, 57, 31, 4, 9, 24, 43, 27, 59, 29, 6, 17, 20, 44, 23, 22, 34, 53, 35, 52, 19, 0, 63, 30, 61, 7, 38, 49, 48, 60, 1, 46, 5, 55, 50, 8, 3, 40, 58, 36, 15, 62, 47, 14, 12],
        [43, 28, 21, 62, 39, 35, 33, 30, 63, 57, 26, 8, 19, 32, 23, 6, 16, 38, 5, 60, 53, 56, 37, 3, 48, 11, 18, 34, 22, 25, 0, 46, 47, 52, 51, 59, 42, 9, 24, 31, 50, 61, 2, 20, 15, 29, 17, 1, 49, 40, 55, 13, 4, 12, 10, 41, 14, 58, 54, 7, 36, 27, 44, 45],
        [21, 9, 57, 35, 19, 41, 3, 8, 30, 47, 42, 23, 52, 18, 15, 59, 11, 37, 54, 25, 53, 51, 56, 44, 16, 46, 26, 12, 43, 2, 28, 14, 38, 29, 10, 61, 1, 45, 7, 39, 13, 6, 27, 5, 60, 22, 17, 4, 49, 55, 36, 0, 62, 63, 31, 32, 24, 48, 40, 34, 33, 20, 58, 50],
        [43, 45, 51, 26, 10, 9, 18, 55, 3, 33, 38, 59, 32, 35, 0, 41, 15, 25, 60, 44, 57, 61, 52, 4, 24, 47, 54, 58, 34, 36, 30, 12, 42, 53, 46, 8, 20, 14, 6, 39, 2, 7, 27, 21, 29, 50, 48, 31, 40, 11, 49, 17, 1, 28, 22, 23, 19, 5, 56, 62, 13, 16, 63, 37],
        [12, 9, 28, 13, 29, 63, 10, 39, 48, 15, 32, 0, 19, 1, 34, 25, 46, 50, 45, 2, 22, 33, 26, 7, 58, 20, 27, 11, 18, 21, 59, 62, 14, 52, 40, 8, 23, 57, 38, 41, 35, 5, 4, 49, 31, 60, 37, 16, 61, 51, 6, 56, 36, 43, 54, 55, 24, 17, 3, 42, 53, 44, 30, 47],
        [29, 62, 32, 17, 52, 13, 34, 46, 48, 51, 54, 20, 3, 63, 41, 56, 19, 44, 16, 58, 6, 37, 59, 0, 28, 33, 53, 47, 21, 12, 9, 25, 40, 26, 4, 1, 61, 42, 60, 18, 10, 31, 2, 7, 49, 23, 45, 15, 11, 30, 39, 8, 50, 55, 24, 14, 43, 27, 36, 57, 38, 35, 5, 22],
        [52, 31, 10, 18, 59, 33, 63, 44, 1, 61, 28, 5, 39, 26, 34, 12, 56, 16, 15, 43, 13, 2, 55, 9, 37, 8, 11, 0, 42, 50, 36, 51, 54, 48, 22, 23, 46, 32, 60, 47, 24, 4, 40, 17, 19, 30, 49, 29, 62, 58, 27, 35, 57, 20, 21, 6, 3, 41, 7, 14, 38, 45, 25, 53],
        [48, 49, 22, 56, 5, 43, 25, 9, 37, 19, 28, 55, 54, 59, 31, 46, 40, 11, 30, 8, 4, 61, 51, 18, 24, 57, 15, 17, 44, 58, 42, 3, 47, 60, 27, 39, 33, 20, 62, 35, 45, 23, 36, 2, 13, 10, 1, 0, 6, 38, 53, 14, 63, 16, 29, 52, 7, 12, 34, 26, 50, 21, 41, 32],
        [26, 14, 56, 29, 51, 61, 15, 54, 2, 63, 30, 40, 62, 27, 52, 4, 0, 21, 13, 38, 33, 53, 5, 8, 39, 36, 47, 57, 58, 43, 7, 60, 1, 9, 25, 28, 24, 55, 23, 41, 45, 49, 12, 10, 22, 35, 11, 6, 50, 16, 32, 31, 44, 37, 48, 42, 46, 59, 34, 3, 18, 20, 17, 19]]

final = [19, 51, 8, 10, 33, 40, 59, 61, 43, 15, 20, 3, 41, 56, 62, 46, 60, 34, 16, 54, 1, 7, 31, 29, 0, 35, 24, 17, 28, 42, 49, 52, 37, 48, 18, 55, 39, 14, 13, 11, 57, 6, 30, 9, 58, 45, 2, 12, 27, 53, 22, 5, 50, 38, 23, 4, 63, 36, 26, 44, 25, 47, 21, 32]

final_inv = [final.index(i) for i in range(64)]

def permute(inp,perm,order=1):
    for _ in range(order):
        inp = [inp[perm[i]] for i in range(64)]
    return inp

def cycle_length(perm):
    t = list(range(64))
    count = 1
    while True:
        t = permute(t,perm)
        if t==list(range(64)):
            return count
        count+=1

gen_all = []
for g in gens:
    t = list(range(64))
    t = permute(t,g)
    while t!=list(range(64)):
        gen_all.append(t)
        t = permute(t,g)



def fixed_points(perm):
    return [i for i in range(len(perm)) if perm[i]==i]

class Phash:
    def init(self):
        self.state = bytearray(range(N))

    def apply_perm(self,perm):
        tmp = bytearray(N)
        for i in range(N):
            tmp[i] = self.state[perm[i]]
        self.state = tmp[:]

    def update(self,ptext):
        if isinstance(ptext,(str)):
            # if hexadecimal string provided, convert to bytes
            ptext = bytes.fromhex(ptext)
        for b in ptext:
            u = (b&0xf0)>>4
            l = (b&0x0f)
            self.apply_perm(gens[u])
            self.apply_perm(gens[l])
        
    def finalize(self):
        self.apply_perm(final)

    def definalize(self):
        self.apply_perm(final_inv)
    
    def give_hash_state(self,given_hash):
        pint = int(given_hash,16)
        self.state = kthperm(pint)
        self.definalize()
        return self.state
        
    def hash_length_extension(self,given_hash,extension):
        pint = int(given_hash,16)
        self.state = kthperm(pint)
        self.definalize()
        self.update(extension)
        self.finalize()
        return self.to_binary()

    
    def h(self,ptext):
        if isinstance(ptext,(str)):
            ptext = bytes.fromhex(ptext)
        self.init()
        self.update(ptext)
        self.finalize()
        return self.to_binary()

    def h_partial(self,ptext):
        self.init()
        self.update(ptext)
        return self.state

    def to_binary(self):
        pint = 0
        nval = list(range(N))
        for i in range(N,1,-1):
            pint+=nval[self.state[N-i]]
            pint*=i-1
            for j in range(self.state[N-i],N):
                nval[j]-=1
        return long_to_bytes(pint).hex()

P = Phash()

def to_binary(state:list):
    pint = 0
    nval = list(range(N))
    for i in range(N,1,-1):
        pint+=nval[state[N-i]]
        #print(nval[state[N-i]])
        pint*=i-1
        for j in range(state[N-i],N):
            nval[j]-=1
    return pint

def kthperm(k):
    S = list(range(64))
    P = []
    while S != []:
        f = factorial(len(S)-1)
        i = k//f
        x = S[i]
        k = k%f
        P.append(x)
        S = S[:i] + S[i+1:]
    return P

def Bruteforce(hash_val):
    hash_state = P.give_hash_state(hash_val)
    for i in tqdm(range(256**3)):
        if P.h_partial(long_to_bytes(i))==hash_state:
            return long_to_bytes(i).hex()

#hashed = {}
#for i in tqdm(range(256**1)):
#    hashed[int(P.h(long_to_bytes(i)),16)]=i
#with open('hashes.pickle','rb') as f:
#    hashed = pickle.load(f)

def bruteforce_cached(hash_val):
    s = list(P.give_hash_state(hash_val))
    return s in gen_all
    
    #return hashed.get(int(hash_val,16),None)

import pwn
HOST,PORT = "permhash296-f1071410.challenges.bsidessf.net", 4560
REM = pwn.remote(HOST,PORT)
i=0
while True:
    i+=1
    print(i)
    REM.sendline(b'challenge 6')
    challenge = REM.recvuntil(b'pre-image?')
    hash_val = re.search(b'[a-f0-9]{74}',challenge)[0].decode()
    x = bruteforce_cached(hash_val)
    if x:
        print(x)
        break
    else:
        REM.sendline()
REM.interactive()
#REM.interactive()


#'00'*780

