from pwn import remote
import gmpy2
import re

HOST, PORT = "jh2i.com", 50013
REM = remote(HOST, PORT)

data = REM.recvuntil(b'What is the PIN?')
print(data.decode())
e_n = re.search(b'(\d+),(\d+)',data)
e = int(e_n[1])
n = int(e_n[2])
PIN = int(re.search(b'is (\d+)',data)[1])

def factor(n,e):
    a = gmpy2.iroot(n+1,2)[0]
    phi = (a-2)*(a)
    return gmpy2.invert(e,phi)

DECRYPTED_PIN = pow(PIN, factor(n,e), n)
REM.sendline(str(DECRYPTED_PIN).encode())
print(REM.recvline().decode())
print(REM.recvline().decode())
print(REM.recvline().decode())
