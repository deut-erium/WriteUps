from Crypto.Util.number import *
from pwn import remote

HOST, PORT = "crypto.challs.pragyanctf.tech", 5002
REM = remote(HOST,PORT)

G = int(REM.recvline().strip().split()[-1])
REM.recvuntil(':')
REM.sendline('1')


ptXr = int(REM.recvline().strip().split()[-1])
REM.recvuntil(':')
REM.sendline('2')
eight_ptXr2 = int(REM.recvline().strip().split()[-1])



# G = int(input('G=\n'))
# ptXr = int(input('enc for s=1 =\n'))
# eight_ptXr2 = int(input('enc for s=2 =\n'))


ptXr2 = (inverse(8,G)*eight_ptXr2)%G
r = (inverse(ptXr,G)*ptXr2)%G
pt = (inverse(r,G)*ptXr)%G

print(long_to_bytes(pt))
