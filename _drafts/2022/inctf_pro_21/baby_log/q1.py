from Crypto.Util.number import *

from flag1 import flag 

flag=bytes_to_long(flag.encode())

p=getPrime(2048)

enc=pow(1-(p*flag),flag,p**4) 

with open('out1.txt','w') as f:
		f.write('enc ='+ hex(enc)+'\n')
		f.write('p= '+hex(p)+'\n')
