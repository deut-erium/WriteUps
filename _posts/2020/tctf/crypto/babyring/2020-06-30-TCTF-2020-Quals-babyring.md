---
title: "0CTF/TCTF 2020 Crypto - babyring"
tags: 0CTF 2020 cryptography sagemath rc4 PoW gaussian_elimination GF2
key: keys
aside:
  toc: true
sidebar:
  nav: aboutnav
author: deuterium
mathjax: false
mathjax_autoNumber: false
mermaid: false
chart: false
show_edit_on_github: true
comment: false
show_author_profile: true
excerpt_separator: <!--more-->
---

# Babyring

## Description
```
nc pwnable.org 10001
```
## Files
- [ring.tar.gz](ring_1f0f741fcfdfc52519d7b09b78c97b43.tar.gz)
  - [release/task.py](release/task.py)

task.py reads (trimming most part)
```python
#!/usr/bin/python2
import os,random,sys,string
from hashlib import sha256
from struct import pack, unpack
import SocketServer
from Crypto.Cipher import ARC4

from flag import flag

K = 64

def gen():
    from Crypto.Util.number import getStrongPrime
    e = 65537
    Ns = []
    for i in range(K):
        p = getStrongPrime(2048)
        q = getStrongPrime(2048)
        Ns.append(p*q)
    return e,Ns

e,Ns = 65537,#list trimmed[...]
class Task(SocketServer.BaseRequestHandler):
    def proof_of_work(self):
        proof = ''.join([random.choice(string.ascii_letters+string.digits) for _ in xrange(20)])
        digest = sha256(proof).hexdigest()
        self.request.send("sha256(XXXX+%s) == %s\n" % (proof[4:],digest))
        self.request.send('Give me XXXX:')
        x = self.request.recv(10)
        x = x.strip()
        if len(x) != 4 or sha256(x+proof[4:]).hexdigest() != digest:
            return False
        return True

    def handle(self):
        if not self.proof_of_work():
            return
        self.request.settimeout(3)
        try:
            self.request.sendall("message: ")
            msg = self.request.recv(0x40).strip()
            ys = []
            for i in range(K):
                self.request.sendall("x%d: " % i)
                x = int(self.request.recv(0x40).strip())
                ys.append(pow(x,e,Ns[i]))
            self.request.sendall("v: ")
            v = int(self.request.recv(0x40).strip())

            key = sha256(msg).digest()[:16]
            E = ARC4.new(key)
            cur = v
            for i in range(K):
                pt = (ys[i]^cur)%(1<<64)
                ct = unpack('Q', E.encrypt(pack('Q',pt)))[0]
                cur = ct

            if cur == v:
                self.request.sendall("%s\n" % flag)
            self.request.sendall("fin\n")
        finally:
            self.request.close()


class ThreadedServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass


if __name__ == "__main__":
    HOST, PORT = '0.0.0.0', 10001
    server = ThreadedServer((HOST, PORT), Task)
    server.allow_reuse_address = True
    server.serve_forever()
```
The first part is obviously proof of work, in which we have to find 4 bytes `XXXX` such that
`sha256(XXXX + 16-char-val) = sha256_hash` for provided `16-char-val` postfix and `sha256_hash`  
Which is easy to solve
> using permutations may not always work (in case of repeated characters), earlier I used combinations_with_replacement which had some weird issues which I could not debug
```python
from hashlib import sha256
import string
from itertools import permutations as take
CHARSET_SHA = string.printable[:62].encode() #0-9a-zA-Z as in challenge

def pow_sha(postfix, hash_val):
    for prefix in take(CHARSET_SHA, 4):
        prefix_bytes = bytes(prefix)
        shaa = sha256(prefix_bytes+postfix).hexdigest()
        if shaa == SHA_256_HASH:
            return prefix_bytes

HOST, PORT = "pwnable.org", 10001
REM = remote(HOST, PORT)
SHA_CHALL = REM.recvuntil(b'XXXX:')
#print(SHA_CHALL.decode())
SHA_256_HASH = re.search(b"[0-9a-f]{64}",SHA_CHALL).group(0).decode()
POSTFIX_STR = re.search(b"[0-9a-zA-Z]{16}",SHA_CHALL).group(0)
PREFIX_CHALL = pow_sha(POSTFIX_STR, SHA_256_HASH)
REM.send(PREFIX_CHALL)
```

Now comes the main part of the challenge, in which we have to provide 64 `xi` values a message `msg` and a value `v`  
The `msg` is sha256 hashed and first 16 bytes are taken to form the `key` for `ARC4`  
The value `v` is XORed with last 64 bits of `pow(x[i], e, Ns[i])` and then `ARC4` encrypted. The goal is to produce the final value equal to the input `v`.  

Since `ARC4` is simply a stream cipher, and encryption is just XORing the plaintext with a keystream, our final value `cur` is essentially `v^ys[0]^...ys[63]^xors[0]^xors[1]...^xors[63]`, where `ys[0..63]` are the last 64 bits of the respective `y[0..63]`  and `xors[0]^xors[1]...^xors[63]` part is essentially dependent on `key` and an invariant for a given `key`, lets call it `invariant(key)` (bye bye `ARC4`).  
All we need to do is to find `x[0..63]` such that `ys[0]^ys[1]...^ys[63] == invariant(key)` and we will have `cur==v` for all `v` as a consequence.

```python
from Crypto.Cipher import ARC4
from hashlib import sha256
from struct import pack, unpack

def encrypt_64(v,key,y):
    E = ARC4.new(key)
    cur = v
    for i in range(64):
        pt = (cur^y[i])%(1<<64)
        ct = unpack('Q',E.encrypt(pack('Q',pt)))[0]
        cur = ct
    return cur

def invariant(key):
    key_val = sha256(key).digest()[:16]
    return encrypt_64(0,key_val,[0 for i in range(64)])

print(invariant(b'aaa'))
# 911494890333775973
```
One could simply put `x[i]` as some value such that `ys[i] == invariant` and all other `xs == 0` but only if one could solve ANY of the RSA by factoring 4096 bit `Ns`, which is obviously not feasible!


Not knowing much linear algebra, I found this [stackexchange post](https://cs.stackexchange.com/questions/53331/minimal-basis-for-set-of-binary-vectors-using-xor/53337#53337) and [this](https://math.stackexchange.com/questions/2054271/gaussian-elimination-gf2) showing all that needs to be done is to have a set of 64 64-bit vectors, and we can represent any 64 bit value using xor of a subset of the vectors. Taking the corresponding `ys` for `xs = 2` for all `i`, and solving the subset for given invariant, we will only set `x[i] = 2` in the `i` in subset else `x[i]=0` (to have no effect).

Sagemath ftw! [CoCalc](https://cocalc.com/app) for the poor
```python
#Ns not shown here
last_64 = [pow(2,e,i)%(1<<64) for i in Ns]
invariant = 911494890333775973 #for msg = b'aaa'
I = GF(2**64)
last_64_mat = [ list(map(int, bin(i)[2:].zfill(64))) for i in last_64  ]
mat = matrix(I,last_64_mat)
invariant_vec = list(map(int, bin(invariant)[2:].zfill(64)))
invariant_vec = matrix(I,invariant_vec)
op = mat.solve_left(invariant_vec)
print(op[0])
```
 Awesome! we have
`(0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 1, 0, 1, 0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 1)` as our output vector, we just have to return `xi` as `2*op` and we are done ;)
 
```python
xs = (0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 1, 0, 1, 0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 1)
xs = [2*i for i in xs]
REM.recv()
REM.send(b'aaa') #message
for i in range(64):
    REM.send(str(xs[i]).encode()) #xi's
    REM.recv()

REM.send(b'0') #v any v would do the job ;)
REM.recv()
#flag{babbbcbdbebfbgbhbibjbkblbmbnbobpbqbrbsbtbubvbwbxby}
```
Unorganized code in files [solve.py](solve.py), [part2.sage](part2.sage) and [test.py](test.py)

### flag{babbbcbdbebfbgbhbibjbkblbmbnbobpbqbrbsbtbubvbwbxby}

