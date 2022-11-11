import pwn
from Crypto.Util.number import long_to_bytes
from Crypto.Cipher import AES
import pwn
import hashlib
HOST, PORT = "crypto1.q21.ctfsecurinets.com", 13337

p =0xf18d09115c60ea0e71137b1b35810d0c774f98faae5abcfa98d2e2924715278da4f2738fc5e3d077546373484585288f0637796f52b7584f9158e0f86557b320fe71558251c852e0992eb42028b9117adffa461d25c8ce5b949957abd2a217a011e2986f93e1aadb8c31e8fa787d2710683676f8be5eca76b1badba33f601f45
g = 2

def decrypt(flag,secret):
    flag = bytes.fromhex(flag)
    iv,flag = flag[:16],flag[16:]
    key = hashlib.sha1(long_to_bytes(secret)).digest()[:16]
    return AES.new(key,AES.MODE_CBC,iv).decrypt(flag)


REM = pwn.remote(HOST,PORT)

ga = eval(REM.recvline().strip().split(b': ')[-1])
gab, nonce1= eval(REM.recvline().strip().split(b': ')[-1])
gb = eval(REM.recvline().strip().split(b': ')[-1])

REM.sendline(str(gab))
gabc, nonce2= eval(REM.recvline().strip().split(b': ')[-1])
nonce2 = gabc^nonce1^1
REM.sendline(str(p-1)+" "+str(nonce2))

gc = eval(REM.recvline().strip().split(b': ')[-1])
REM.sendline(str(gc))
gca = eval(REM.recvline().strip().split(b': ')[-1])
REM.sendline(str(gca)+" "+str(nonce1))

enc_flag = REM.recvall().split()[-1].decode()
if enc_flag.isalnum():
    print(decrypt(enc_flag,gabc^nonce1))

#Securinets{master-in-the-middle_bb8f4b012d02284aea258723179dff83}
