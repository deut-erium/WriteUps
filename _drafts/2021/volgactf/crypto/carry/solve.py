from fcsr import *
import gmpy2
import re

def repeat(seq):
    return list(set(re.findall(br'(.+?)(?=\1)',seq)))



q = 509
q = int(gmpy2.next_prime(10**4))
k = int(math.log(q+1,2))
random.seed()
a = random.randint(1,2**k-1)
test = FCSR(q,0,a)
sequence = test.encrypt(b'\x00'*100000)
#lam,mu = floyd(sequence,sequence[0])
#print("cycle_size:",mu,"start",lam)


