from base64 import b64decode
from itertools import zip_longest, combinations,cycle
from collections import Counter
from tqdm import tqdm

def xor(a,b):
    if len(a)<len(b):
        a,b = b,a
    return bytes([i^j for i,j in zip(a,cycle(b))])


MAX_KEYSIZE = 36000

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

with open('chal1-30c8fd72a1c8184c80c35a4626e0cdfc.enc','rb') as ct_file:
    ct = ct_file.read()

#ct = b64decode(b''.join(data.split()))

def hamming_distance(str1:bytes, str2:bytes)->int:
    n1 = bin(int.from_bytes(str1,'big'))[2:]
    n2 = bin(int.from_bytes(str2,'big'))[2:]
    return [i==j for i,j in zip_longest(n1,n2)].count(False)    

def find_key_size(ct:bytes)->list:
    norm_distances = []
    for KEYSIZE in tqdm(range(2,min(MAX_KEYSIZE,len(ct)//4))):
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

key_len = 1363
key = find_key(ct,key_len)
pt = xor(ct,key)

plaintext=b"""The Infinite Improbability Drive was a wonderful  new  method  of crossing        interstellar  distances in  a mere nothingth of a second, without all that tedious mucking about in hyperspace."
It was discovered by   lucky chance and  then  developed  into  a governable  form  of  propulsion  by  the  Galactic  Government's research team on Damogran.
 This, briefly, is the story of its discovery. 
The principle of generating small amounts of finite improbability
by  simply  hooking  the  logic circuits of a Bambleweeny 57 Sub-
Meson Brain to an atomic vector plotter  suspended  in  a  strong
Brownian  Motion  producer  (say  a  nice hot cup of tea) were of
course well understood - and such generators were often  used  to
break  the  ice  at  parties  by  making all the molecules in the
hostess's undergarments leap simultaneously one foot to the left,
in accordance with the Theory of Indeterminacy. 
Many respectable physicists said that they weren't going to stand
for  this  -  partly  because it was a debasement of science, but
mostly because they didn't get invited to those sort of parties. 
Another thing they couldn't stand was the perpetual failure they  encountered in trying to construct a machine which could generate the infinite improbability  field  needed  to  flip  a  spaceship across  the mind-paralyzing distances between the farthest stars, and in the end they grumpily announced that such a machine was virtually impossible."""

#for i in range(0,1400,20):
#    print(pt[i:i+20])
#    print(plaintext[i:i+20])


key = xor(ct,plaintext[:1363])[:1363]
pt = xor(ct,key)
with open('plaintext.txt','wb') as f:
    f.write(pt)

#bctf{lcm_c0m37_to_th3_r35cue!!}


#probable_keys = [find_key(ct,s[0]) for s in find_key_size(ct)]
#probable_keys = [find_key(ct,i) for i in range(1,)]
#for key in probable_keys:
#    try:
#        pt = xor(ct,key).decode()
#        if pt.isprintable():
#            print(pt)
#    except:
#        continue

