from math import gcd
import gmpy2

def xgcd(a,b):
    a1=1; b1=0; a2=0; b2=1; aneg=1; bneg=1
    if(a < 0):
        a = -a; aneg=-1
    if(b < 0):
        b = -b; bneg=-1
    while True:
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



N1= 97047969232146954924046774696075865737213640317155598548487427318856539382020276352271195838803309131457220036648459752540841036128924236048549721616504194211254524734004891263525843844420125276708561088067354907535207032583787127753999797298443939923156682493665024043791390402297820623248479854569162947726288476231132227245848115115422145148336574070067423431126845531640957633685686645225126825334581913963565723039133863796718136412375397839670960352036239720850084055826265202851425314018360795995897013762969921609482109602561498180630710515820313694959690818241359973185843521836735260581693346819233041430373151
e1= 3
c1= 6008114574778435343952018711942729034975412246009252210018599456513617537698072592002032569492841831205939130493750693989597182551192638274353912519544475581613764788829782577570885595737170709653047941339954488766683093231757625

p2= 7237005577332262213973186563042994240829374041602535252466099000494570602917
q2= 88653318322320212121171535397276679450159832009631056842709712756058489880609
e2= 16
c2= 128067909105216284348808993695734979917384615977985008857494038384160720721127262500602107681721675827823420594821881043967947295783995842628815275429540

N3= 3213876088517980551083924185487283336189331657515992206038949
e3= 65537
c3= 2941293819923490843589362205798232424837846370982721175905966


m1 = gmpy2.iroot(c1,e1)
if m1[1]:
    m1 = int(m1[0])

m2_probables = set()
for m_pow_8 in rabin_decrypt(c2,p2,q2):
    for m_pow_4 in rabin_decrypt(m_pow_8,p2,q2):
        for m_pow_2 in rabin_decrypt(m_pow_4,p2,q2):
            for m2_probable in rabin_decrypt(m_pow_2,p2,q2):
                m2_probables.add(m2_probable)

m2_prefix = "28322C".lower()
for i in m2_probables:
    if hex(i)[2:].startswith(m2_prefix):
        m2 = i

p3 = 1267650600228229401496703205653
q3 = N3//p3
m3 = pow(c3, pow(e3,-1,(p3-1)*(q3-1)), N3)

