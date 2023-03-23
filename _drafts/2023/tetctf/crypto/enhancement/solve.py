import pwn
from Crypto.Util.number import *
import base64
signs = []
for _ in range(50):
    REM = pwn.remote("192.53.115.129", 31340)
    # REM = pwn.process("./enhancement", shell=True)
    REM.sendline(bytes(43))
    m = bytes_to_long(base64.b64decode(REM.recvline().strip()[3:]+b'=' ))
    r = bytes_to_long(base64.b64decode(REM.recvline().strip()[3:]+b'=' ))
    s = bytes_to_long(base64.b64decode(REM.recvline().strip()[3:]+b'=' ))
    signs.append((m,r,s))
    REM.close()


from ecdsa.ecdsa import curve_secp256k1, generator_secp256k1
G = generator_secp256k1
q = G.order()
B = 2**(256-8)
NUM = len(signs)
M = matrix(QQ, NUM+2, NUM+2)


for i,(m,r,s) in enumerate(signs):
    M[i,i] = q
    M[NUM, i] = mod(r*inverse(s, q), q)
    M[NUM+1, i] = -mod(m*inverse(s, q), q)

M[NUM, NUM] = QQ(B)/QQ(q)
M[NUM+1, NUM+1] = QQ(B)

rows = M.LLL()
for row in rows:
    d = ((QQ(-(row[-2])) * q) / B) % q
    REM = pwn.remote("192.53.115.129", 31340)
    # REM = pwn.process("./enhancement", shell=True)
    dbytes = int(d).to_bytes(32,'big')
    print(dbytes.hex())
    REM.sendline(base64.b64encode(dbytes))
    data = REM.recv()
    if b"No way" in data:
        print(data)
        break
    REM.close()
