from decimal import Decimal, getcontext
from fractions import Fraction
from Crypto.Util.number import bytes_to_long, getRandomNBitInteger,long_to_bytes
import contfrac
import sympy

getcontext().prec=1000

x = getRandomNBitInteger(128)
xx = str( Decimal(x).sqrt() )
real_r,real_j = xx.split('.')
f = Decimal('0.'+real_j[:60])

def rest_n(R,f):
    rest = int(R.sqrt())
    rest_new = (R-rest**2-f**2)/(2*f)
    return rest_new



# N = r**2 + 2*r*x + x**2


# print(x)
# input()
# R=Decimal(2**127)
# while True:
#     r_new = rest_n(R,f)
#     R_new = (r_new+f)**2
#     diff = float(R_new-R)
#     print(diff)
#     R=R_new


# R = Decimal('2.0')
# r = int(R.sqrt())
# while True:
#     diff = R-(r**2+f**2+2*r*f)
#     print(diff)
#     r = int(R.sqrt())
#     r1 = (R-r**2-f**2)/(2*f)
#     R1 = ( r1**2+f**2+2*r1*f ).sqrt()
#     R = R1 

m = b'My cryptographic message.'
m = [int(i) for i in str(bytes_to_long(m))]
enc_m = [int(i,16) for i in '6a6185a7719127d0a6355e5e51d83926562f0ca70f80744b146bb467c4b3']
fstream = [i^j for i,j in zip(enc_m,m)]
F = Decimal("0."+"".join(map(str,fstream)))
enc_flag = [int(i,16) for i in '55172e0833b3e9ed4be2c610e0d151ba2395141b7d0b4327451061c4b6213264fa979636b080c6028438a3b6515502111c82251cd25b0761c6514764682']

xor_lookup = [[] for _ in range(16)]
for i in range(10):
    for j in range(10):
        xor_lookup[i^j].append((i,j))

cont = list(contfrac.continued_fraction(Fraction(F),10000))

poss = []

x = sympy.Symbol('x')
for j in range(2,100):
    e=1/x
    for i in cont[::-1][:j]:
        e = i+1/e
    numer,denom = e.as_numer_denom()
    quad = x*denom - numer
    poss.append(list(sympy.roots(quad))[0])



def decrypt(stream):
    stream = [int(i) for i in stream]
    flag = [i^j for i,j in zip(enc_flag,stream[60:])]
    flag = int("".join(map(str,flag)))
    return long_to_bytes(flag)



#[0, 4, 1, 1, 5, 1, 4, 3, 3, 1, 1, 1, 1, 3, 1, 1, 2, 1, 2, 5+x]
