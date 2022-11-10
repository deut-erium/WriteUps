from ec import *
from hashlib import md5
import pwn
from os import urandom
import string
HOST, PORT = "52.59.124.14", 10005

def hashmd5(msg):
    return int(md5(msg).hexdigest(),16)


p = 0xffffffff00000001000000000000000000000000ffffffffffffffffffffffff
a = -3
b = 0x5ac635d8aa3a93e7b3ebbd55769886bc651d06b0cc53b0f63bce3c3e27d2604b
q = 0xffffffff00000000ffffffffffffffffbce6faada7179e84f3b9cac2fc632551
B = 2**128

curve = EllipticCurve(p,a,b, order=q)
G = ECPoint(curve, 0x6b17d1f2e12c4247f8bce6e563a440f277037d812deb33a0f4a13945d898c296, 0x4fe342e2fe1a7f9b8ee7eb4a7c0f9e162bce33576b315ececbb6406837bf51f5)

REM = pwn.remote(HOST, PORT)
REM.recvline()
P_a = REM.recvline().split(b',')
P_a = ECPoint(curve, int(P_a[0][6:]), int(P_a[1][1:-2]))
REM.recvuntil(b'\n\n')

def get_sign(msg):
    REM.sendline(b'1:'+msg)
    data = REM.recvuntil(b'\n\n')
    print(data)
    return eval(data.split(b'\n')[0])


def sign(msg : bytes, d_a):
        k = int(md5(os.urandom(16)).hexdigest()[:4], 16)
        R = G*k
        x,y = R.x, R.y
        r = x % q
        s = inverse(k, q) * (int(md5(msg).hexdigest(),16) + r * d_a) % q
        return r,s

ri_s, si_s, mi_s = [],[],[]

for _ in range(4):
    msg = "".join(choice(string.ascii_letters) for _ in range(10)).encode()
    mi_s.append(hashmd5(msg))
    r,s = get_sign(msg)
    ri_s.append(r)
    si_s.append(s)

ti_s, ai_s = [], []
for r,s,m in zip(ri_s, si_s, mi_s):
    s_inv = pow(s,-1,q)
    ti_s.append((r*s_inv)%q)
    ai_s.append((-m*s_inv)%q)

num_sigs = len(mi_s)
M = matrix(QQ,num_sigs+2, num_sigs+2)
for i in range(len(mi_s)):
    M[i,i] = q
    M[-2, i] = ti_s[i]
    M[-1, i] = ai_s[i]

M[-1,-1] = B
M[-2,-2] = B/q

rows = M.LLL()
for row in rows:
    d = ((QQ(-(row[-2])) * q) / B) % q
    if (G*d).x == P_a.x:
        print('asdfasdf')
        break

target = b'I still love cookies.'

signature = sign(target, d)

REM.sendline("2:{},{}".format(*signature).encode())
print(REM.recvuntil(b'\n\n'))


#ENO{gr33tings_fr0m_the_PS3}






