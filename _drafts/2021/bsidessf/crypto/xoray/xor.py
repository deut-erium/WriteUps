from base64 import b64decode
from itertools import zip_longest, combinations
from pwn import xor
from collections import Counter

MAX_KEYSIZE = 40

FREQ_DIST = Counter({
    'a': 0.0651738,
    'b': 0.0124248,
    'c': 0.0217339,
    'd': 0.0349835,
    'e': 0.1041442,
    'f': 0.0197881,
    'g': 0.0158610,
    'h': 0.0492888,
    'i': 0.0558094,
    'j': 0.0009033,
    'k': 0.0050529,
    'l': 0.0331490,
    'm': 0.0202124,
    'n': 0.0564513,
    'o': 0.0596302,
    'p': 0.0137645,
    'q': 0.0008606,
    'r': 0.0497563,
    's': 0.0515760,
    't': 0.0729357,
    'u': 0.0225134,
    'v': 0.0082903,
    'w': 0.0171272,
    'x': 0.0013692,
    'y': 0.0145984,
    'z': 0.0007836,
    ' ': 0.1918182 
})

with open('xoray.bin','rb') as ct_file:
    ct = ct_file.read()

#ct = b64decode(b''.join(data.split()))

def hamming_distance(str1:bytes, str2:bytes)->int:
    n1 = bin(int.from_bytes(str1,'big'))[2:]
    n2 = bin(int.from_bytes(str2,'big'))[2:]
    return [i==j for i,j in zip_longest(n1,n2)].count(False)    

def find_key_size(ct:bytes)->list:
    norm_distances = []
    for KEYSIZE in range(2,min(MAX_KEYSIZE,len(ct)//4)):
        blocks = [ct[i:i+KEYSIZE] for i in range(0,KEYSIZE*4,KEYSIZE)]
        dist_arr = [hamming_distance(i,j)/KEYSIZE for i,j in combinations(blocks,2)]
        dist = sum(dist_arr)/len(dist_arr)
        norm_distances.append((KEYSIZE,dist))
    return sorted(norm_distances,key = lambda x:x[1])

def single_byte_key(ct:bytes)->list:
    return Counter(ct).most_common(1)[0][0]^ord(FREQ_DIST.most_common(1)[0][0])

def find_key(ct, key_len):
    key = bytearray(key_len)
    for i in range(key_len):
        key[i] = single_byte_key(ct[i::key_len])
    return bytes(key)

KEY = find_key(ct, find_key_size(ct)[0][0])
with open('output.html','wb') as f:
    f.write(xor(ct,KEY))

#CTF{this_is_why_k4_remains_unsolved}
#print(xor(ct,KEY))
