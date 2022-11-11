from flag import flag
from Crypto.Util.number import bytes_to_long, getPrime
from random import randbytes, getrandbits

msg=b'copper copper copper copper copper copper copper copper!'
assert len(flag)==103

def pad(msg,l):
    return msg+randbytes(l-len(msg))

e=[3,65537]
p,q=getPrime(1024),getPrime(1024)
n=p*q

assert n.bit_length()==2048

k=(n+getrandbits(16))>>2

m1=bytes_to_long(pad(flag,110))
m2=bytes_to_long(pad(flag,110))

c=pow(bytes_to_long(msg),e[1],n)

c1=pow(m1,e[0],n)
c2=pow(m2,e[0],n)

with open('out.txt','w') as f:
    f.write('k = ' + hex(k)+'\n')
    f.write('c = ' + hex(c)+'\n')
    f.write('c1 = '+ hex(c1)+'\n')
    f.write('c2 = ' + hex(c2)+'\n')
