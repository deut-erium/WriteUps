import pwn
HOST, PORT = "secureroots.2021.3k.ctf.to", 13371
from gmpy2 import is_square
from hashlib import sha256
import random
from math import gcd


def randbytes(n):
    return int.to_bytes(random.getrandbits(n*8),n,'big')


REM = pwn.remote(HOST,PORT)
data = REM.recvregex(b'u : (\d+)\n\nUsername :')
re_pat = b'Public modulus : (\d+)\n\nUsername : Guest\nr : (\d+)\nu : (\d+)\n'
vals = pwn.re.search(re_pat,data).groups()
N,r,u = map(int,vals)

m = b'Guest'
c = int.from_bytes( sha256(m+int.to_bytes(u,20,'big')).digest(),'big')
p = gcd(pow(r,2)-c,N)
q = N//p

def xgcd(a,b):
    a1=1; b1=0; a2=0; b2=1; aneg=1; bneg=1
    if(a < 0):
        a = -a; aneg=-1
    if(b < 0):
        b = -b; bneg=-1
    while (1):
        quot = -(a // b)
        a = a % b
        a1 = a1 + quot*a2; b1 = b1 + quot*b2
        if(a == 0):
            return (b, a2*aneg, b2*bneg)
        quot = -(b // a)
        b = b % a;
        a2 = a2 + quot*a1; b2 = b2 + quot*b1
        if(b == 0):
            return (a, a1*aneg, b1*bneg)

def SqrRoots(a,n):
    def inverse_mod(a,n):
        (g,xa,xb) = xgcd(a,n)
        return xa % n
    def TSRsqrtmod(a,grpord,p):
        ordpow2=0; non2=grpord
        while(not ((non2&0x01)==1)):
            ordpow2+=1; non2//=2
        for g in range(2,grpord-1):
            if (pow(g,grpord//2,p)!=1):
                break
        g = pow(g,non2,p)
        gpow=0; atweak=a
        for pow2 in range(0,ordpow2+1):
            if(pow(atweak,non2*2**(ordpow2-pow2),p)!=1):
                gpow+=2**(pow2-1)
                atweak = (atweak * pow(g,2**(pow2-1),p)) % p
        d = inverse_mod(2,non2)
        tmp = pow(a*pow(g,gpow,p),d,p)
        return (tmp*inverse_mod(pow(g,gpow//2,p),p)) % p
    x1=TSRsqrtmod(a,n-1,n)
    return x1,-x1%n

def rabin_decrypt(CT,p,q):
    n=p*q
    mp1,mp2=SqrRoots(CT,p)
    mq1,mq2=SqrRoots(CT,q)
    _,yp,yq=xgcd(p,q)
    r1=(yp*p*mq1+yq*q*mp1)%n
    r2=(yp*p*mq1+yq*q*mp2)%n
    r3=(yp*p*mq2+yq*q*mp1)%n
    r4=(yp*p*mq2+yq*q*mp2)%n
    return [r1,r2,r3,r4]


def decrypt(c):
    mp = pow(c, (p + 1) // 4, p)
    mq = pow(c, (q + 1) // 4, q)
    _, yp, yq = xgcd(p, q)
    r = (yp * p * mq + yq * q * mp) % (N)
    return r

def sign(m):
    U = randbytes(20)
    c = int(sha256(m + U).hexdigest(), 16)
    r = rabin_decrypt(c,p,q)[0]
    return (r, int(U.hex(), 16))

def verify(m, r, u):
    U = int.from_bytes(u,'big')
    c = int(sha256(m + U).hexdigest(), 16)
    return c == pow(r, 2, N)

r1,u1 = sign(b'3k-admin')

REM.sendline('3k-admin')
REM.sendline(str(r1))
REM.sendline(str(u1))
data = REM.recvall()
ct = int(pwn.re.search(b'Message : (\d+)\n',data)[1])
mm = pow(ct,pow(0x10001,-1,(p-1)*(q-1)),N)
print(mm.to_bytes((mm.bit_length()+7)//8,'big'))
#
#CTF{f4ulty_s1gn4ture_f41l}
