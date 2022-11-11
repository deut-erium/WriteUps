import pwn
import random
from Crypto.Util.number import getStrongPrime,inverse
import re
from collections import Counter
from tqdm import tqdm

HOST,PORT = "crypto.ctf.zer0pts.com", 10463

def k(n,p):
    if pow(n,(p-1)//2,p)==1:
        return 1
    return -1

def find_conn():
    pwn.context(log_level=0)
    while True:
        REM = pwn.remote(HOST,PORT)
        REM.recvline()
        pub_key_data = REM.recvline()
        pwn.context(log_level=1000)
        g = int(re.search(b'g: (\d+),',pub_key_data)[1])
        p = int(re.search(b'p: (\d+)\n',pub_key_data)[1])
        if k(g,p)==1 and not all(k(i,p)==1 for i in range(1,4) ):
            pwn.context(log_level=0)
            return REM,p,g
        else:
            REM.close()


def get_chall(REM):
    chall = REM.recvuntil(b'hand(1-3):')
    c1,c2 = eval(re.search( b'commitment is=(\(.*\))',chall)[1])
    return c1,c2

def send_out(res,REM):
    #1 Rock, 2 scissors 3 paper
    REM.sendline(str(res))
    result = REM.recvuntil(b'[system]')
    res = None
    if b'My hand is ... Scissors' in result:
        res =  2
    if b'My hand is ... Rock' in result:
        res =  1
    else:
        res =  3
    if b'draw' in result:
        return 'draw',res
    elif b'You win' in result:
        return 'win',res
    else:
        return 'loser',res
    #    print('draw')
    #elif b'You win' in result:
    #    print('win')
    #else:
    #    print('loser')

#1:rock, 2:scissors, 3:paper
#1, (3, 2)
#2, (1, 3)
#3, (2, 1)
#
def best_move(c2,residues):
    res = k(c2,p)
    if residues == [1,1,-1]:
        if res==-1:
            return 2
        else:
            return 1
    elif residues == [1,-1,1]:
        if res==-1:
            return 1
        else:
            return 3

i=0
REM,p,g = find_conn()
residues = [k(i,p) for i in (1,2,3)]

while True:
    c2 = get_chall(REM)[1]
    best = best_move(c2,residues)
    response,opp = send_out(best,REM)
    print(i,response)
    i+=1

def commit(m, key):
    (g, p), (x, _) = key
    r = random.randint(2, p-1)
    c1 = pow(g, r, p)
    c2 = m * pow(g, r*x, p) % p
    return c2

def keygen(size):
    p = getStrongPrime(size)
    g = random.randint(2, p-1)
    x = random.randint(2, p-1)
    return (g, p), (x, p)

def test():
    key = keygen(1024);g,p=key[0]
    x=k(g,p)
    if x==1:
        min_pow_2=max(i for i in range(6) if g%2**i==0)
        min1 = min(i for i in range(1,7) if k(commit(1,key),p,i)!=1)
        min2 = min(i for i in range(1,7) if k(commit(2,key),p,i)!=1)
        min3 = min(i for i in range(1,7) if k(commit(2,key),p,i)!=1)
        return min_pow_2,min1,min2,min3
    return 0,0,0,0

#zer0pts{jank3n-jank3n-0ne-m0r3-batt13}

#c = Counter()
#c1 = Counter()
#for i in tqdm(range(700)):
#    t = test()
#    c[t]+=1
#    c1[t[1:]]+=1
#c=Counter({(0, 0, 0, 0): 211, (0, 2, 1, 1): 25, (0, 2, 2, 2): 24, (1, 2, 1, 1): 15, (0, 3, 1, 1): 14, (1, 2, 2, 2): 12, (2, 2, 1, 1): 11, (2, 2, 2, 2): 9, (1, 3, 1, 1): 7, (0, 4, 2, 2): 7, (3, 2, 1, 1): 7, (2, 3, 1, 1): 5, (3, 3, 1, 1): 4, (0, 4, 4, 4): 3, (3, 2, 2, 2): 3, (1, 4, 2, 2): 3, (0, 2, 2, 3): 3, (1, 5, 3, 3): 2, (0, 5, 2, 2): 2, (1, 5, 2, 2): 2, (4, 3, 1, 1): 2, (1, 4, 3, 3): 2, (0, 4, 3, 2): 1, (4, 4, 3, 3): 1, (0, 2, 2, 4): 1, (8, 2, 2, 2): 1, (1, 3, 2, 2): 1, (2, 4, 4, 4): 1, (0, 7, 2, 2): 1, (2, 3, 4, 4): 1, (5, 4, 3, 3): 1, (3, 6, 3, 3): 1, (1, 4, 4, 4): 1, (0, 3, 4, 3): 1, (1, 3, 3, 3): 1, (5, 2, 1, 1): 1, (2, 6, 3, 3): 1, (7, 5, 2, 2): 1, (4, 2, 1, 1): 1, (5, 3, 1, 1): 1, (6, 2, 2, 2): 1, (8, 3, 1, 1): 1, (5, 6, 4, 4): 1, (0, 3, 3, 4): 1, (0, 3, 4, 4): 1, (1, 3, 4, 2): 1, (0, 3, 3, 3): 1, (0, 5, 5, 5): 1, (0, 4, 3, 3): 1})
#c1=Counter({(0, 0, 0): 211, (2, 1, 1): 60, (2, 2, 2): 50, (3, 1, 1): 34, (4, 2, 2): 10, (4, 4, 4): 5, (4, 3, 3): 5, (5, 2, 2): 5, (2, 2, 3): 3, (5, 3, 3): 2, (3, 4, 4): 2, (6, 3, 3): 2, (3, 3, 3): 2, (4, 3, 2): 1, (2, 2, 4): 1, (3, 2, 2): 1, (7, 2, 2): 1, (3, 4, 3): 1, (6, 4, 4): 1, (3, 3, 4): 1, (3, 4, 2): 1, (5, 5, 5): 1})
REM.interactive()



