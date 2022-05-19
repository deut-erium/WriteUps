from pwn import remote
from sympy import factorint

HOST, PORT = "crypto.zh3r0.ml", 8451
REM = remote(HOST, PORT)

n = int(REM.recvline().strip()[2:])
e = int(REM.recvline().strip()[2:])
c = int(REM.recvline().strip()[3:])

p, q = factorint(n)
phi = (p-1)*(q-1)
d = pow(e, -1, phi)
m = pow(c, d, n)

print(bytes.fromhex(hex(m)[2:]).decode())
