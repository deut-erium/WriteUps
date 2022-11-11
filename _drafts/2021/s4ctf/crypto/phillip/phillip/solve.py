import pwn
from gmpy2 import isqrt

HOST, PORT = "157.90.231.113",9999

REM = pwn.remote(HOST,PORT)

REM.sendline('G')

params = REM.recvregex(b'params = \(.*\)\n')
n,f,v = eval( pwn.re.search(b'params = (\(.*\))',params).group(1) )

def factorize(n,f):
    for v in range(2,10000,2):
        phi = f*v
        p = ((n+1-phi)+isqrt( ((n+1-phi)**2)-4*n))//2
        if n%p==0:
            return int(p),int(n//p)

p,q = factorize(n,f)

def get_hash(num):
    REM.sendline("T")
    REM.sendline(str(num))
    hashdata = REM.recvregex(b'phillip_hash\(m\) = (\d+)\n')
    hashval = int(pwn.re.search(b'phillip_hash\(m\) = (\d+)\n',hashdata).group(1))
    return hashval

val1 = pow(p+q,1,n**2)
val2 = pow(p+q,n+1,n**2)
print(val1,val2)

REM.sendline('R')
REM.sendline(str(val1))
REM.sendline(str(val2))
print(REM.recvregex(b'S4CTF\{.*\}'))

#S4CTF{A94In__pr0b4b1liStiC__aSymM37r1c_Al9OriThm!!}
