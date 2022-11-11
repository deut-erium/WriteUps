from Crypto.Util.number import *
from secret import *
p=getPrime(1024)
q=getPrime(1024)
n=p*q
e=65537
e1=5**e 
e2=7**e
m=bytes_to_long(flag)
c1=pow(m,e1,n)
c2=pow(m,e2,n)
f=open('common.txt','wb')
f.write('c1 ='+str(c1)+'\n')
f.write('c2 ='+str(c2)+'\n')
f.write('n ='+str(n)+'\n')
