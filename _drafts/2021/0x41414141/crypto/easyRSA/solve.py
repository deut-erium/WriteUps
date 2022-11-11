from sympy import factorint
from collections import Counter
from Crypto.Util.number import long_to_bytes

c = 3708354049649318175189820619077599798890688075815858391284996256924308912935262733471980964003143534200740113874286537588889431819703343015872364443921848
e = 16
p = 75000325607193724293694446403116223058337764961074929316352803137087536131383
q = 69376057129404174647351914434400429820318738947745593069596264646867332546443

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
        if(g != 1): raise ValueError("***** Error *****: {0} has no inverse (mod {1}) as their gcd is {2}, not 1.".format(a,n,g))
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

def rsa_dec(CT,e,p,q):
    return pow(CT,pow(e,-1,(p-1)*(q-1)),p*q)

def gen_rsa_dec(CT,e,p,q):
    phi = (p-1)*(q-1)
    n = p*q
    facs = list(Counter(factorint(e)).elements())
    results = [CT]
    prod=1
    for fac in facs:
        if fac==2:
            new_res = []
            for result in results:
                new_res.extend(rabin_decrypt(result,p,q))
            results = list(set(new_res))
        elif gcd(fac,phi)!=1:
            return []
        else:
            new_res = []
            for result in results:
                new_res.append(rsa_dec(result,fac,p,q))
            results = new_res.copy()
        prod*=fac
        results = [i for i in results if pow(i,prod,n)==CT]
    return results

for pt in gen_rsa_dec(c,e,p,q):
    print(long_to_bytes(pt))

