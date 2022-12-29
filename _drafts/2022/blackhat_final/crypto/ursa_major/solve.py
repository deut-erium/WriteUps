from Crypto.Util.number import isPrime, getPrime, inverse
from secrets import randbelow
from sympy import nextprime, primerange
import hashlib, time, os
import pwn

REM = pwn.process("python3.11 ursamajor.py",shell=True)
REM.sendline()
data = REM.recvuntil(b'[Q]uit\n|\n|  >')

def r():return int.from_bytes(os.urandom(512//8))

flag_e = int(data.split(b'\n')[15].split()[-1])
e = [int(pwn.re.findall(b'e  = (\d+)\n',data)[1])]

# for _ in range(10):
#     REM.sendline(b'u')
#     data = REM.recvuntil(b'[Q]uit\n|\n|  >')
#     e.append(int(pwn.re.search(b'e  = (\d+)\n',data)[1]))

f =r()
es = []
for _ in range(10000):
    es.append(r()%f)


# HOST, PORT = "",



# PBIT, LBIT = 256, 12
# def prime_gen(pbit=PBIT, lbit=LBIT):
#     B = 2**lbit
#     while True:
#         q, qlst = 1, []
#         while q.bit_length() < pbit - 1:
#             qlst.append(nextprime(randbelow(min([B, 2**(pbit - q.bit_length())]))))
#             q *= qlst[-1]
#         if len(qlst) != len(set(qlst)):
#             continue
#         Q = 2 * q + 1
#         if isPrime(Q):
#             break
#     print(len(qlst))
#     print(qlst)
#     print(sorted(qlst))

