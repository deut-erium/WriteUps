from itertools import product
from tqdm import tqdm

class Hash:
    H = bytearray(b'RITSEC')
    def __init__(self,X:bytes):
        for x in X:
            self.hash_x(x)

    def hash_x(self,Xi:int):
        for r in range(13):
            Hi = bytearray(6)
            Hi[1] = self.H[0]
            Hi[4] = (self.H[0] + self.H[5])%256
            Hi[3] = self.H[1]>>5
            Hi[2] = (self.H[3]<<2)%256
            Hi[5] = self.H[3]
            k = (self.H[2]^self.H[4])&self.H[5]
            k1 = (k+self.H[1] + (self.H[3]<<2)%256)%256
            Hi[0] = (r+Xi+k1)%256
            self.H = Hi

    def digest(self):
        return self.H.hex()

assert Hash(b'RITSEC_CTF_2021').digest()=='3ba50807aa02'

target = '435818055906'
#for test in product(range(256),repeat=3):
#    if Hash(test).digest()==target:
#        print(bytes(test))

with open('/home/deuterium/yo/wordlists/rockyou.txt','rb') as f:
    data = map(lambda x: x.strip(),f.readlines())

for p in tqdm(data):
    if Hash(p).digest()==target:
        print(p)
