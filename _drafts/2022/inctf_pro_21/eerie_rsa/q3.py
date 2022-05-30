from Crypto.Util.number import *
from gmpy2 import *
from dummy import flag
p=getPrime(224)
q=getPrime(800)
d=q+45
n=p*q
phi=(p-1)*(q-1)
#assert gcd(d,phi)==8
#assert n.bitlength()==1024
e=inverse(d,(p-1)*(q-1))
ct=pow(bytes_to_long(flag),e,n)
with open('out3.txt','w') as f :
	f.write('n =' + str(n) + '\n')
	f.write('e =' + str(e) + '\n')
	f.write('ct ='+ str(ct) + '\n')

