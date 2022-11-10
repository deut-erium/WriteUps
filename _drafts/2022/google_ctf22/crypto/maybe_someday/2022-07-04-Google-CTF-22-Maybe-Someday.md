---
title: "Google CTF 2022 Crypto - Maybe Someday"
tags: googlectf 2022 cryptography paillier padding oracle
key: googlectf2022maybesomeday
description: >
    Google CTF 2022 cryptography writeup maybe someday
    paillier cryptosystem homomorphic padding oracle
aside:
  toc: true
sidebar:
  nav: aboutnav
author: deuterium
full_width: false
mathjax: true
mathjax_autoNumber: true
mermaid: false
chart: false
show_edit_on_github: true
comment: false
show_author_profile: true
excerpt_separator: <!--more-->
---

TLDR; Leaking 20 bits of information from custom padding oracle using
homomorphic properties of paillier cryptosystem

<!--more-->

## Challenge Description
### Maybe Someday [240 points] (solved by 35)
> Leave me your ciphertexts. I will talk to you later.  
> `maybe-someday.2022.ctfcompetition.com 1337`  
> [attachment](https://storage.googleapis.com/gctf-2022-attachments-project/73c2725dabd614c5fdd6e6a347493e177428a2a80744bd4225490480dd894ecc2607068a8f07bf96f6c7d540869dc36ba3f4d60bf510812ec86649a1bc306dd0)  

## Files
> [attachment.zip](./attachment.zip)  
> - [chall.py](./chall.py)  

### Not Included
> [/flag.txt](./flag.txt)

## Server Source
```python
from Crypto.Util.number import getPrime as get_prime
import math
import random
import os
import hashlib

# Suppose gcd(p, q) = 1. Find x such that
#   1. 0 <= x < p * q, and
#   2. x = a (mod p), and
#   3. x = b (mod q).
def crt(a, b, p, q):
    return (a*pow(q, -1, p)*q + b*pow(p, -1, q)*p) % (p*q)

def L(x, n):
    return (x-1) // n

class Paillier:
    def __init__(self):
        p = get_prime(1024)
        q = get_prime(1024)

        n = p * q
        λ = (p-1) * (q-1) // math.gcd(p-1, q-1) # lcm(p-1, q-1)
        g = random.randint(0, n-1)
        µ = pow(L(pow(g, λ, n**2), n), -1, n)

        self.n = n
        self.λ = λ
        self.g = g
        self.µ = µ

        self.p = p
        self.q = q

    # https://www.rfc-editor.org/rfc/rfc3447#section-7.2.1
    def pad(self, m):
        padding_size = 2048//8 - 3 - len(m)

        if padding_size < 8:
            raise Exception('message too long')

        random_padding = b'\0' * padding_size
        while b'\0' in random_padding:
            random_padding = os.urandom(padding_size)

        return b'\x00\x02' + random_padding + b'\x00' + m

    def unpad(self, m):
        if m[:2] != b'\x00\x02':
            raise Exception('decryption error')

        random_padding, m = m[2:].split(b'\x00', 1)

        if len(random_padding) < 8:
            raise Exception('decryption error')

        return m

    def public_key(self):
        return (self.n, self.g)

    def secret_key(self):
        return (self.λ, self.µ)

    def encrypt(self, m):
        g = self.g
        n = self.n

        m = self.pad(m)
        m = int.from_bytes(m, 'big')

        r = random.randint(0, n-1)
        c = pow(g, m, n**2) * pow(r, n, n**2) % n**2

        return c

    def decrypt(self, c):
        λ = self.λ
        µ = self.µ
        n = self.n

        m = L(pow(c, λ, n**2), n) * µ % n
        m = m.to_bytes(2048//8, 'big')

        return self.unpad(m)

    def fast_decrypt(self, c):
        λ = self.λ
        µ = self.µ
        n = self.n
        p = self.p
        q = self.q

        rp = pow(c, λ, p**2)
        rq = pow(c, λ, q**2)
        r = crt(rp, rq, p**2, q**2)
        m = L(r, n) * µ % n
        m = m.to_bytes(2048//8, 'big')

        return self.unpad(m)

def challenge(p):
    secret = os.urandom(2)
    secret = hashlib.sha512(secret).hexdigest().encode()

    c0 = p.encrypt(secret)
    print(f'{c0 = }')

    # # The secret has 16 bits of entropy.
    # # Hence 16 oracle calls should be sufficient, isn't it?
    # for _ in range(16):
    #     c = int(input())
    #     try:
    #         p.decrypt(c)
    #         print('😀')
    #     except:
    #         print('😡')

    # I decided to make it non-interactive to make this harder.
    # Good news: I'll give you 25% more oracle calls to compensate, anyways.
    cs = [int(input()) for _ in range(20)]
    for c in cs:
        try:
            p.fast_decrypt(c)
            print('😀')
        except:
            print('😡')

    guess = input().encode()

    if guess != secret: raise Exception('incorrect guess!')

def main():
    with open('flag.txt', 'r') as f:
      flag = f.read()

    p = Paillier()
    n, g = p.public_key()
    print(f'{n = }')
    print(f'{g = }')

    try:
        # Once is happenstance. Twice is coincidence...
        # Sixteen times is a recovery of the pseudorandom number generator.
        for _ in range(16):
            challenge(p)
            print('💡')
        print(f'🏁 {flag}')
    except:
        print('👋')

if __name__ == '__main__':
    main()
```

DISCLAIMER: This writeup is attempted to be written in a way such that a naive
reader who is yet to see or attempt the challenge can make sense out of the writeup.  
Feel free to skip any sections which you understand already 
{:.info}


## Understanding the challenge
- The challenge server deploys the [Paillier Cryptosystem](https://en.wikipedia.org/wiki/Paillier_cryptosystem)
- A single instance `p` of `Paillier` is used throught the connection and public key 
`(n, g)` is provided
- We are required to solve `challenge(p)` 16 times successfully to get the flag

### `challenge(p)`
- A two-byte `secret` is selected randomly which is then hashed to its 
sha512 hexdigest byte-string of length 128 hexadecimal characters
  - if selected secret = `b'\x00\x00'`, 
  - `hashlib.sha512(secret).hexdigest().encode()` = `b'5ea71dc6d0b4f57bf39aadd07c208c35f06cd2bac5fde210397f70de11d439c62ec1cdf3183758865fd387fcea0bada2f6c37a4a17851dd1d78fefe6f204ee54'`
  - 20 integer inputs taken together after which the server returns 20 outputs 
  whether decryption succeeded for each of the inputs `'😀'` for success and `'😡'` for failure
  - After 20 inputs, it requests for a `guess` for `secret` if the guess matches, we are good to go

### Understanding Decryption
- `fast_decrypt(c)` is same as `decrypt(c)`. The only difference being the way 
`r = pow(c, λ, n**2)` is calculated using [Chinese Remainder Theorem](https://en.wikipedia.org/wiki/Chinese_remainder_theorem) (just for speed considerations and no effect on the workings of the challenge)
- All steps will proceed in decryption of arbitrary integer `c`, just the last
`self.unpad(m)` which will fail if `m` is not in desired padding format.

### Understanding Padding/Unpadding
#### Valid Padding Structure
```
+----------+---------------------+------+---------+
| \x00\x02 | RANDOM_NONNULL_DATA | \x00 | message |
+----------+---------------------+------+---------+
```
Where  
- The first two bytes are 0 and 2 respectively
- `RANDOM_NONNULL_DATA` is a random string constructed form bytes `[1,255]`
of length `2048//8 - 3 (for \x00\x02 and \x00) - len(message)` = `253 - len(message)` >= 8
i.e. from `[8,253]` (funnily enough message can be null)
- A null byte spearating `RANDOM_NONNULL_DATA` from our `message`
- Our `message` of length `[0,245]` from restriction on size of padding

While unpadding, the server just checks if these conditions are satisfied 
and raises exception otherwise.






