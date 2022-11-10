# Begin POW
import base64
import tqdm
from operator import truediv
import secrets
import sys

try:
    import gmpy2
    HAVE_GMP = True
except ImportError:
    HAVE_GMP = False
    sys.stderr.write("[NOTICE] Running 10x slower, gotta go fast? pip3 install gmpy2\n")

VERSION = 's'
MODULUS = 2**1279-1
CHALSIZE = 2**128

SOLVER_URL = 'https://goo.gle/kctf-pow'

def python_sloth_root(x, diff, p):
    exponent = (p + 1) // 4
    for i in range(diff):
        x = pow(x, exponent, p) ^ 1
    return x

def python_sloth_square(y, diff, p):
    for i in range(diff):
        y = pow(y ^ 1, 2, p)
    return y

def gmpy_sloth_root(x, diff, p):
    exponent = (p + 1) // 4
    for i in range(diff):
        x = gmpy2.powmod(x, exponent, p).bit_flip(0)
    return int(x)

def gmpy_sloth_square(y, diff, p):
    y = gmpy2.mpz(y)
    for i in range(diff):
        y = gmpy2.powmod(y.bit_flip(0), 2, p)
    return int(y)

def sloth_root(x, diff, p):
    if HAVE_GMP:
        return gmpy_sloth_root(x, diff, p)
    else:
        return python_sloth_root(x, diff, p)

def sloth_square(x, diff, p):
    if HAVE_GMP:
        return gmpy_sloth_square(x, diff, p)
    else:
        return python_sloth_square(x, diff, p)

def encode_number(num):
    size = (num.bit_length() // 24) * 3 + 3
    return str(base64.b64encode(num.to_bytes(size, 'big')), 'utf-8')

def decode_number(enc):
    return int.from_bytes(base64.b64decode(bytes(enc, 'utf-8')), 'big')

def decode_challenge(enc):
    dec = enc.split('.')
    if dec[0] != VERSION:
        raise Exception('Unknown challenge version')
    return list(map(decode_number, dec[1:]))

def encode_challenge(arr):
    return '.'.join([VERSION] + list(map(encode_number, arr)))

def get_challenge(diff):
    x = secrets.randbelow(CHALSIZE)
    return encode_challenge([diff, x])

def solve_challenge(chal):
    [diff, x] = decode_challenge(chal)
    y = sloth_root(x, diff, MODULUS)
    return encode_challenge([y])
# End POW

def solve(ms, coins):
    # return list of machine - coins
    # coins are in sorted order of (id, value)
    res = [None] * len(ms)
    # CODE HERE
    return res

from pwn import *

conn = remote("35.204.95.14", 1337)
conn.recvuntil(b'with:\n')
cm = conn.recvline().decode().strip()[52:]
pow_res = solve_challenge(cm)
print(pow_res)
conn.recvuntil(b"Solution? ")
conn.sendline(pow_res.encode())
conn.recvuntil(b'Correct\n')

for machine in range(1, 13):
    print(conn.recvuntil(f"Machine {machine}:\n".encode()))
    conn.sendline(b"Display")
    conn.recvline()
    ms = []
    for _ in range(56):
        ms.append(int(conn.recvline().decode().strip().split(": ")[1]))
    print(ms)
    conn.recvline()
    conn.recvline()
    coins = []
    for _ in range(200):
        coins.append(int(conn.recvline().decode().strip().split(": ")[1]))
    print(coins)
    conn.recvline()
    conn.recvline()
    # coins = [(i+1, coins[i]) for i in range(len(coins))]
    # coins.sort(key=lambda y: y[1])
    res = solve(ms, coins)
    for i in range(len(res)):
        ins = "Insert " + "".join(str(q) + " " for q in res[i])
        print(ins)
        conn.sendline(ins.encode())
        for _ in range(len(res[i])):
            conn.recvline()
        conn.sendline(f"Buy {i+1}".encode())
        print(conn.recvline().decode())
conn.interactive()
