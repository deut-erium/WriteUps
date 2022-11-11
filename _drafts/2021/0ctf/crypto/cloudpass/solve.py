import pwn
import string
from hashlib import sha256
from itertools import product

POW_CHARSET = (string.ascii_letters+ string.digits).encode()

HOST, PORT = "111.186.59.1", 10001

REM = pwn.remote(HOST, PORT)

def solve_pow(chall,hash_out):
    for comb in product(POW_CHARSET,repeat=4):
        if sha256(bytes(comb)+chall).hexdigest()==hash_out:
            return bytes(comb)

pow_chall = REM.recvuntil(b'XXXX:')

pow_chall,pow_hash = pwn.re.search(b'\+(.*)\) == ([0-9a-f]{64})',pow_chall).groups()
REM.sendline(solve_pow(pow_chall,pow_hash.decode()))
REM.interactive()
