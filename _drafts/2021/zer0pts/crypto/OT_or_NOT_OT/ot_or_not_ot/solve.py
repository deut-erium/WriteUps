import pwn
HOST, PORT = "crypto.ctf.zer0pts.com", 10130
from tqdm import tqdm

from Crypto.Cipher import AES
from Crypto.Util.number import long_to_bytes

REM = pwn.remote(HOST,PORT)
pwn.context(log_level=1000)
enc_flag = pwn.base64.b64decode(REM.readline().strip().split(b': ')[1])
p = int(REM.readline().strip().split(b'= ')[1])
bit_len = int(REM.readline().strip().split(b'= ')[1])

def decrypt(key,enc_flag):
    key = long_to_bytes(key)
    cip = AES.new(key,AES.MODE_CBC,iv = enc_flag[:16])
    return cip.decrypt(enc_flag[16:])

#
def get(a,b,c,d):
    REM.sendlineafter(b'a = ',str(a))
    REM.sendlineafter(b'b = ',str(b))
    REM.sendlineafter(b'c = ',str(c))
    REM.sendlineafter(b'd = ',str(d))

    x = int(REM.readline().strip().split(b'= ')[1])
    y = int(REM.readline().strip().split(b'= ')[1])
    z = int(REM.readline().strip().split(b'= ')[1])
    return x,y,z

key = 0
for bit_pox in range(bit_len//2):
    t = int(REM.readline().strip().split(b'= ')[1])
    x,y,z = get(t**3%p,t**4%p,t,t**2%p)
    # x = 3r+s, y = 4r+s, d = 2r+s
    # yx-1==xz-1
    for i in range(2):
        for j in range(2):
            u,v=x^i,y^j
            #print((pow(u,-1,p)*v)%p,(pow(z,-1,p)*u)%p)
            if (pow(u,-1,p)*v)%p == (pow(z,-1,p)*u)%p:
                print(bit_pox,i,j)
                key<<=2
                key+=2*i+j
            #else:
                #print("hmmm")
key2 = key2 = int(bin(key)[2:].zfill(256)[::-1],2)
print(decrypt(key2,enc_flag))
REM.interactive()
