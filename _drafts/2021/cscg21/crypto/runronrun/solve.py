import pwn
from collections import Counter
from multiprocessing import Pool

HOST,PORT = "7b000000d4a8d5ef5d35dd64-runronrun.challenge.broker.cscg.live", 31337
from tqdm import tqdm
REM = pwn.remote(HOST,PORT,ssl=True)
from functools import reduce
from operator import add
#REM = pwn.process('main.py')
#pwn.context(log_level=0)
REM.recvuntil('>')
def get(offset,REM):
    REM.sendline(str(offset))
    hexc = REM.recvuntil('>')[:(26-2*offset)].decode()
    return bytes.fromhex(hexc)


def make_counter(i):
    #REM = pwn.remote(HOST,PORT,ssl=True)
    REM = pwn.process('main.py')
    REM.recvuntil('>')
    c = Counter([get(i,REM)[1] for _ in tqdm(range(10000))])
    REM.close()
    return c

with Pool(10) as p:
    x = reduce(add,p.map(make_counter,[10]*10))

CSCG{schn ieke
#CSCG{schnieke}
#flag = bytearray(13)
#for i in range(12):
#    ciphertexts = Counter([get(i)[1] for _ in tqdm(range(10000))])
#    flag[i+1] = ciphertexts.most_common()[0][0]
#    print(flag)


#c = Counter([get(12)[1] for i in range(400)] )
#
