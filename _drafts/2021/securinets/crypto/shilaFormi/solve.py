import pwn
import re
import random
from gmpy2 import jacobi
HOST,PORT = "crypto2.q21.ctfsecurinets.com" ,1337
REM = pwn.remote(HOST,PORT)
pwn.context(log_level=0)

#balance = 10
#while True:
#    REM.sendline(str(balance))
#    chall = REM.recvuntil(b'Shilaaafooooooormi:')
#    modulus = re.search(b'wallet is (\d+).*\n\nPublic Modulus : (\d+)\n\n.*Here\'s my choice : (\d+)\n',chall)
#    wallet,n,choice = int(modulus[1]),int(modulus[2]),int(modulus[3])
#    if jacobi(choice,n)==-1:
#        print('saxisaxisaxisaxi')
#        REM.sendline(b'1')
#    else:
#        if n%8 in (3,5):
#            REM.sendline(b'0')
#        else:
#            REM.sendline(b'1')
#    balance*=2
while True:
    chall = REM.recvuntil(b'Place your bet :')
    wal_mod = re.search(b'wallet is (\d+).*\n\nPublic Modulus : (\d+)\n',chall)
    balance, n = int(wal_mod[1]), int(wal_mod[2])
    if n%8 in (3,5):
        REM.sendline(str(balance))
    else:
        REM.sendline(b'1')
    chall = REM.recvuntil(b'Shilaaafooooooormi:')
    choice = int(re.search(b'my choice : (\d+)\n',chall)[1])
    if jacobi(choice,n)==-1:
        REM.sendline(b'1')
    else:
        REM.sendline(b'0')

#Securinets{You_got_s0_lucky!_or_did_you?_e48382bbad3c0f1e6be924d0d19c796b}
