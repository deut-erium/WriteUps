import math
n =  101603423619327484271263737680483903006810757724406340113788486892385159544832779663758816137458690872326975229773549832050570427456026570535133325297487188056622187108195169358887249902761248071043303974742936275538121504962556748410886202674914152058123706709672344559529461453829821421451848837206175525869
S =  6823099836394897740742060913705878607569974589643289781331356626982135007521866621082508488325642435147531391

def keygen2(ln):
    X = [2]
    x = 2
    for i in range(ln):
        x = 2 * x + 1
        X.append(x)
    return X


UPPER_LIMIT = 1000
X = keygen2(UPPER_LIMIT)
selected = [0]*len(X)

for i in range(UPPER_LIMIT-1,-1,-1):
    if S>=X[i]:
        S-=X[i]
        selected[i]=1

assert S==0
C_len = max(i*selected[i] for i in range(UPPER_LIMIT))
C_enc = selected[:C_len+1]
C_enc = ''.join(map(str,C_enc))

h = int(math.log(int(math.log(n,2)),2))

def encrypt1(m,h,n):
    while len(m)%h!=0:
        m = '0'+ m
    l = len(m) // h
    r = 89657896589
    x=pow(r,2,n)
    C = ''
    for i in range(l):
        x = pow(x,2,n)
        p_i = (bin(x)[2:])[-h:]
        c_i = int(p_i,2)^int(m[i*h:(i+1)*h],2)
        cx = bin(c_i)[2:].zfill(h)
        C+=cx
    return C

m = encrypt1(C_enc,h,n)
print(bytes.fromhex(hex(int(m,2))[2:]))
