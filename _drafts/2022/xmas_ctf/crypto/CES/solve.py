import pwn
import random
from nltk.corpus import words
import string
from collections import Counter

WORDS = words.words()
MOD = 677

def get_plaintext(word_cnt):
    plaintext = ""
    for i in range(word_cnt):
        plaintext += random.choice(WORDS)
    return plaintext

def chr2int(x):
    return ord(x) - ord("a") + 1

def int2chr(x):
    return chr(x + ord("a"))

def to_chars(ct):
    if ct == 676:
        return "##"
    else:
        fst = int2chr(ct // 26)
        snd = int2chr(ct % 26)
        return fst + snd

def pad(plaintext):
    if len(plaintext) %  2 != 0:
        return plaintext + "a"
    else:
        return plaintext

class CES(object):
    def __init__(self):
        self.rand_gen = random.SystemRandom()
        self.key = [self.rand_gen.randint(0, MOD - 1) for i in range(5)]
    def encrypt_pair(self, pair):
        x, y = map(chr2int, pair)
        return (x**2 * self.key[0] + x * y * self.key[1] + y**2 * self.key[2] + x * self.key[3] + y * self.key[4]) % MOD
    def encrypt(self, plaintext):
        pt = pad(plaintext)
        ct = ''.join([to_chars(self.encrypt_pair(pt[i: i + 2])) for i in range(0, len(pt), 2)])
        return ct


cs = CES()
pt = get_plaintext(10000).lower()
ct = cs.encrypt(pt)

ct_count = Counter(ct[i:i+2] for i in range(0,len(ct),2))
pt_count = Counter(pt[i:i+2] for i in range(0,len(pt),2))
c_count = Counter(cs.encrypt((i,j)) for i in string.ascii_lowercase for j in string.ascii_lowercase)


# HOST, PORT = "challs.htsp.ro", 10004

# REM = pwn.remote(HOST, PORT)

# for _ in range(4):
#     REM.recvline()

# data = REM.recvline()


