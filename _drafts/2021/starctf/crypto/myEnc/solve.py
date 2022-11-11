from pwn import remote,context
context(log_level=100)
from hashlib import sha256
from itertools import product
import string
from time import time

CHARSET = string.printable[:62].encode()
HOST, PORT = "52.163.228.53", 8081
REM = remote(HOST,PORT)

pow_chall = REM.recvline().strip().split()
REM.recvline()
chall, target = pow_chall[0].split(b'+')[-1][:-1],pow_chall[-1].decode()

def PoW(chall:bytes,target:str):
  for comb in product(CHARSET,repeat=4):
    if sha256(bytes(comb)+chall).hexdigest()==target:
      print(bytes(comb))
      return bytes(comb)

REM.sendline(PoW(chall,target))
n = int(REM.recvline().strip().split()[-1])


flag_len = 15*8
flag = [None for _ in range(flag_len)]
CTS = []
cnt=7
while any(i is None for i in flag):
    REM.recvline()
    REM.sendline(b'0')
    start = time()
    ct = int(REM.recvline().strip().split()[-1])
    end = time()-start
    if end>1:
        flag[cnt]=1
    else:
        flag[cnt]=0 
    # CTS.append((ct,end))
    cnt=(cnt+7)%flag_len
    print(flag)

REM.interactive()
#*CTF{yOuG0t1T!}
