from Crypto.Util.number import *
from gmpy2 import next_prime
p = int(input("p = "))
r = int(input("r = "))

pubkey = eval(input('public_key = '))
msg = input("message = ").encode()
ex_signature = eval(input('signature ='))
forge_m = input("message to forge = ").encode()

l = 5
M = [bytes_to_long(msg[4 * i:4 * (i + 1)]) for i in range(l)]
q = int(next_prime(max(M)))
priv_key_partial = [ ( pow(M[i],-1,q)*ex_signature[i] )%q  for i in range(l)]

def recover_priv(priv_partial,pubkey,p,r,q,d=32):
    i = 0
    while True:
        rs = i*q+priv_partial[0]+pubkey[0]
        s = ( pow(r,-1,p)*rs )%p
        r2s = ( r*r*s )%p
        pv = int(bin(r2s)[2:][:-d]+'0'*d,2)
        ps =  int(bin(r2s)[2:][-d:],2)
        if pv==pubkey[1] and ps%q == priv_key_partial[1]:
            return s
        i+=1

def keygen(r,p,s, l=5, d=32):
    U = [pow(r, c + 1, p) * s % p for c in range(0, l)]
    V = [int(bin(u)[2:][:-d] + '0' * d, 2) for u in U]
    S = [int(bin(u)[2:][-d:], 2) for u in U]
    privkey, pubkey = S, V
    return pubkey, privkey

def sign(msg, privkey, d):
    msg = msg.encode('utf-8')
    l = len(msg) // 4
    M = [bytes_to_long(msg[4 * i:4 * (i + 1)]) for i in range(l)]
    q = int(next_prime(max(M)))
    sign = [M[i] * privkey[i] % q for i in range(l)]
    return sign


s = recover_priv(priv_key_partial,pubkey,p,r,q)
pubkey,privkey = keygen(r,p,s)

forged = sign(forge_m.decode(), privkey, 32)
print(forged)

#CCTF{Lattice_bA5eD_T3cHn1QuE_70_Br34K_LCG!!}
