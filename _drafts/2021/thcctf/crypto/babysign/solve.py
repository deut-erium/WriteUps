import pwn
from sympy import factorint
from Crypto.Util.number import GCD, bytes_to_long, long_to_bytes

HOST, PORT = "remote1.thcon.party", 11001

REM = pwn.remote(HOST,PORT)
#REM = pwn.process('python3 server.py',shell=True)
PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 251]




chall = REM.recvuntil(b'Choice: ')
N = int(pwn.re.search(b'n: (\d+)\n',chall)[1])

signs = {}
for p in PRIMES:
    print("getting signature:",p)
    REM.sendline('1')
    REM.sendline(str(p))
    ret = REM.recvuntil(b'Choice: ')
    sign = int(pwn.re.search(b'Signature: (\d+)\n',ret)[1])
    signs[p] = sign

def forge_sign(n:int):
    forged = 1
    for fac,power in factorint(n).items():
        sign_fac = signs.get(fac,None)
        if not sign_fac:
            return -1
        forged = (forged*pow(sign_fac,power,N))%N
    return forged

def forge_message(m:bytes):
    n = bytes_to_long(m)
    k = forge_sign(n)
    if k!=-1:
        return k
    return None

def facs(m:bytes):
    print(factorint(bytes_to_long(m)))


def send_command(cmd):
    forged = forge_message(cmd)
    if forged:
        REM.sendline('2')
        REM.sendline(cmd)
        REM.sendline(str(forged))
        REM.interactive()
        #recv = REM.recvuntil(b'Choice: ')
        #print(recv.decode())

def is_256_smooth(m:bytes):
    n = bytes_to_long(m)
    while n!=1:
        for p in PRIMES:
            if n%p==0:
                n//=p
                break
        else:
            return False
    return True

def smooth2(n:int):
    for p in PRIMES:
        if n==1:
            return True
        while n%p==0:
            n//=p
    return n==1


#print(forge_message(b'ex *iQP'))
#send_command(b'ex *iQP')
#send_command(b'vi *U\xa1\xac')
send_command(b'vi *tZd')
#SMOOTH = [i for i in range(1,10**6) if smooth2(i)]


#THCon21{Textb00k_RS4_Mall3ab1l1ty}

#from itertools import product
#for i,j,k in product(range(30),repeat=3):
#    message = b' '*i+b'nl'+b' '*j+b'* ;'+b' '*k
#    if is_256_smooth(message):
#        print(i,j,k,message)


#msg = b'|nl *'
#for prefix in product(range(256),repeat=3):
#    if is_256_smooth(bytes(prefix)+msg):
#        print(bytes(prefix))
#    message = b'echo %s;cat flag.txt' % bytes(prefix)
#    if is_256_smooth(message):
#        print(message)
#
