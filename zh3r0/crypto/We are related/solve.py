from pwn import remote
from Crypto.PublicKey import RSA
from base64 import b64decode
import re

HOST, PORT = "crypto.zh3r0.ml", 9841
REM = remote(HOST, PORT)

data = REM.recvuntil(b'0.Exit')
print(data.decode())

REM.sendline(b'1')
pub_key = REM.recvuntil(b'-----END PUBLIC KEY-----\n').strip()

rsa = RSA.importKey(b64decode(pub_key.split(b'\n-----END PUBLIC KEY-----\n')[0].split(b'-----BEGIN PUBLIC KEY-----')[1]))
print(pub_key.decode())

N = rsa.n
E = rsa.e

REM.sendline(b'2')
REM.sendline()
REM.sendline(b'2')
REM.sendline(b'a')
REM.sendline(b'0')
data = REM.recvuntil(b'BYE')
print(data.decode())

c1, c2 = map(int, re.findall(b'(\d+)\n',data))
print("""n = {}
C1 = {}
C2 = {}
e = {}""".format(N,c1,c2,E))

diff = ord('a')
R.<X> = Zmod(n)[]
f1 = X^3 - C1
f2 = (256*X + r)^3 - C2
def my_gcd(a, b):
     return a.monic() if b == 0 else my_gcd(b, a % b)
mint=-my_gcd(f1, f2).coefficients()[0]
# mint = 84490476860330212673060501801652621134953572462322324101674679636525065183282486185148354532461487912067725608302199264119177290786545985493246692410205660189434658580866030237305212940461964070200849268673142227118980326807902129431038850502565588905103675210898161818686994591193583661769377667810413989357162402550803291023005993338743213389843385122094
print(bytes.fromhex(hex(mint)[2:]).decode())
# "RSA is secure and all but the only thing I want to say is zh3r0{Hey_y0u_Sh0u1dn't_S3nd_r3l4ted_m3ssag3s_0r_h4v3_shot_p4ddings_wh3n_e_1s_sm411!!!!!}.

