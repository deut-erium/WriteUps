import re
from random import *
from Crypto.Util.number import *
from hashlib import *
from fastecdsa.curve import secp256k1


with open('output.txt') as f:
    data = f.read().strip().split("\n")

re_pattern = re.compile("b'(.*)', \((\d+), (\d+)\), True")

sigs = []
for line in data[:-1]:
    m, r, s = re.search(re_pattern, line).groups()
    sigs.append((int(sha256(m.encode()).hexdigest(), 16), int(r), int(s)))


def ecc_sign(msg, ecc, privkey):
        z = sha256(msg).hexdigest()
        k = int(z, 16) ^ privkey
        x, y = (k * ecc.G).x, (k * ecc.G).y
        r = x
        s = inverse(k, ecc.q) * (int(z, 16) + r * privkey) % ecc.q
        return (r, s)


ecc = secp256k1
privkey = randrange(ecc.q)
pubkey = privkey* ecc.G
msg = b"adsfasdfasdfasd"
ztest = int(sha256(msg).hexdigest(),16)
rtest, stest = ecc_sign(msg, ecc, privkey)
stestinv = pow(stest, -1, ecc.q)
stinv = (-ztest*stestinv)%ecc.q
rtinv = (-rtest*stestinv)%ecc.q
assert ((ztest^privkey) + stinv + rtinv*privkey)%ecc.q == 0
contstst = []
for i,zi in enumerate(bin(ztest)[2:].zfill(256)[::-1]):
    if zi=='0':
        contstst.append( ((rtinv+1)*(2**i))%ecc.q)
    else:
        stinv = (stinv + 2**i)%ecc.q
        contstst.append( ((rtinv-1)*(2**i))%ecc.q)
privbits = list(map(int, bin(privkey)[2:].zfill(256)))
sump = sum(i*j for i,j in zip(contstst,privbits[::-1]))%ecc.q
assert (sump+stinv)%ecc.q == 0
print( (sump+stinv)//ecc.q)

# pk = BitVec('pk', 512)

eqs = []
# constraints = [ pk>0, pk<ecc.q]
knapsack = []
weights = []

matrix = []
for z,r,s in sigs:
    sinv = pow(s, -1, ecc.q)
    zsinv = (-z*sinv)%ecc.q
    rsinv = (-r*sinv)%ecc.q
    # z^pk + zsinv + rsinv*pk = 0 mod q
    eqs.append((z, zsinv, rsinv))
    constants = []
    # constraints.append(URem(zsinv + rsinv*pk, ecc.q) == z^pk)
    for i,zi in enumerate(bin(z)[2:].zfill(256)[::-1]):
        if zi=='0':
            constants.append( ((rsinv+1)*(2**i))%ecc.q)
        else:
            zsinv = (zsinv + 2**i)%ecc.q
            constants.append( ((rsinv-1)*(2**i))%ecc.q)

    knapsack.append(constants)
    weights.append(zsinv)
    matrix.append(constants+[zsinv+ -ecc.q])

import pickle
with open("matrix.pickle","wb") as f:
    pickle.dump((matrix,weights, knapsack, ecc.q),f)


# pk dot constant[i] + weight[i] = 0  mod q






# z^pk = zs^-1 + rs^-1 pk:wq

