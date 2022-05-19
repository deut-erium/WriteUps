from pwn import remote
from sympy.ntheory.modular import crt
from gmpy2 import iroot

HOST, PORT = "crypto.zh3r0.ml", 7419
n = []
c = []

REM = remote(HOST, PORT)
n.append(int(REM.recvline().strip()[2:]))
c.append(int(REM.recvline().strip()[3:]))
REM.close()
e=2
while True:
    print(e)
    REM = remote(HOST, PORT)
    n.append(int(REM.recvline().strip()[2:]))
    c.append(int(REM.recvline().strip()[3:]))
    resultant, mod = crt(n,c)
    value, is_perfect = iroot(resultant,e)
    if is_perfect:
        print(bytes.fromhex(hex(value)[2:]).decode())
        break
    e+=1
    REM.close()

