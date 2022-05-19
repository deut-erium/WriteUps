from pwn import remote
from gmpy2 import invert

HOST, PORT = "95.216.233.106", 20391

REM = remote(HOST, PORT)

p = int(REM.recvline().decode().strip()[3:])
q = int(REM.recvline().decode().strip()[3:])
e = int(REM.recvline().decode().strip()[3:])
ct = int(REM.recvline().decode().strip()[4:])


PHI = (p - 1) * (q - 1)
D = invert(e, PHI)
MESSAGE = pow(ct, D, p * q)
print(bytes.fromhex(hex(MESSAGE)[2:]).decode())
