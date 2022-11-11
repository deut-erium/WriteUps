import pwn
from gmpy2 import is_prime

pwn.context(log_level=0)
HOST, PORT = "34.73.1.249" ,32703

REM = pwn.remote(HOST, PORT)

M = 310717010502520989590157367261876774703
G = (179210853392303317793440285562762725654, 105268671499942631758568591033409611165)
P = (280810182131414898730378982766101210916, 291506490768054478159835604632710368904)

diff = (P[1]**2-P[0]**3)-(G[1]**2-G[0]**3)
a = (pow(P[0]-G[0],-1,M)*diff)%M
b = (P[1]**2 - P[0]**3 - a*P[0])%M

xx = 15994140035312710196327380901996167841374157

responses = []
for _ in range(144):
    chall = REM.recvregex(b'(\d+): ')
    integer = int(chall.strip().split()[-1].strip(b':'))
    if is_prime(integer):
        REM.sendline(b'y')
        responses.append(1)
    else:
        REM.sendline(b'n')
        responses.append(0)

REM.sendline(b'23fcf62e4ca5319696cfcae39d75860c')

#LOL did you seriously think we would give up the flag that easy?
#Hurry up https://drive.google.com/file/d/1w-MNL-KXLsg5XO6NVF9Av9XM40cpzu3q/view?usp=sharing

REM.interactive()
