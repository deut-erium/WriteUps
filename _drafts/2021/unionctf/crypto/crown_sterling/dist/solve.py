
#!/usr/bin/env python3

#from secrets import flag, musical_key
flag = "".join(chr(i) for i in bytes.fromhex('76f64667220717784affa07cf6b8be52c7d8348d778a41615efa9e53f2566b27fd96eb984c08'))
from tqdm import tqdm
from itertools import product
from bisect import bisect_left
from Crypto.Util.number import isPrime
from functools import lru_cache
import sys
sys.setrecursionlimit(100000)
import math

@lru_cache(None)
def sieve_for_primes_to(n):
    # Copyright Eratosthenes, 204 BC
    size = n//2
    sieve = [1]*size
    limit = int(n**0.5)
    for i in range(1, limit):
        if sieve[i]:
            val = 2*i+1
            tmp = ((size-1) - i)//val
            sieve[i+val::val] = [0]*tmp
    return tuple([2] + [i*2+1 for i, v in enumerate(sieve) if v and i > 0])

@lru_cache(None)
def is_quasi_prime(n, primes):
    # novel class of semi-prime numbers
    # https://arxiv.org/pdf/1903.08570.pdf
    #print(primes)
    p2 = 0
    for p1 in primes:
        if n % p1 == 0:
            p2 = n//p1
            break
    if isPrime(p2) and not p1 in [2, 3] and not p2 in [2, 3]:
        return True
    return False

@lru_cache(None)
def bbp_pi(n):
    #print(n)
    # Bailey-Borwein-Plouffe Formula
    # sounds almost as cool as Blum-Blum-Shub
    # nth hex digit of pi
    @lru_cache(None)
    def S(j, n):
        s = 0.0
        k = 0
        while k <= n:
            r = 8*k+j
            s = (s + pow(16, n-k, r) / r) % 1.0
            k += 1
        t = 0.0
        k = n + 1
        while 1:
            newt = t + pow(16, n-k) / (8*k+j)
            if t == newt:
                break
            else:
                t = newt
            k += 1
        return s + t

    n -= 1
    x = (4*S(1, n) - 2*S(4, n) - S(5, n) - S(6, n)) % 1.0
    return "%02x" % int(x * 16**2)

@lru_cache(None)
def digital_root(n):
    # reveals Icositetragon modalities when applied to Fibonacci sequence
    return (n - 1) % 9 + 1 if n else 0

@lru_cache(None)
def fibonacci(n):
    # Nature's divine proportion gives high-speed oscillations of infinite
    # wave values of irrational numbers
    assert(n >= 0)
    if n < digital_root(2):
        return n
    else:
        return fibonacci(n - 1) + fibonacci(n - 2)


def is_valid_music(music):
    # Leverage music's infinite variability
    assert(all(c in "ABCDEFG" for c in music))


def is_valid_number(D):
    # Checks if input symbolizes the digital root of oxygen
    assert(8==D)


def get_key(motif):
    #is_valid_music(motif)
    #is_valid_number(len(motif))
    # transpose music onto transcendental frequencies
    indexes = [(c)**i for i, c in enumerate(motif)]
    size = sum(indexes)
    assert(size < 75000) # we will go larger when we have quantum
    return indexes, size


@lru_cache(None)
def get_q_grid(size):
    return [i for i in range(size) if is_quasi_prime(i, sieve_for_primes_to(math.floor(math.sqrt(size))+1))]


q_grid = get_q_grid(75000)

for i in tqdm(range(500000)):
    x = bbp_pi(i)

for musical_key in tqdm(product([3,4,5,6,7,1,2],repeat=8),total=7**8):
    #musical_key = "".join(mus)
    #print("[+] Oscillating the key")
    try:
        key_indexes, size = get_key(musical_key)
    except AssertionError:
        continue
    #print("[+] Generating quasi-prime grid")
    #q_grid = get_q_grid(size)
    q_grid_size = bisect_left(q_grid,size)
    # print(f"indexes: {key_indexes}  size: {size}  len(q_grid): {len(q_grid)}")

    out = bytearray()
    for i, p in enumerate(flag):
        #print(f"[+] Entangling key and plaintext at position {i}")
        index = key_indexes[i % len(key_indexes)] * fibonacci(i)
        try:
            q = q_grid[index % q_grid_size]
        except:
            continue
        key_byte_hex = bbp_pi(q)
        # print(f"index: {index:10}  fib: {fibonacci(i):10}  q-prime: {q:10}  keybyte: {key_byte_hex:10}")
        out.append(ord(p) ^ int(key_byte_hex, 16))
    if out.startswith(b'union'):
        print(out)
    #print(f"[+] Encrypted: {bytes(out)}")

#union{b45ed_oN_iRR3fut4bL3_m4th3m4G1c}
