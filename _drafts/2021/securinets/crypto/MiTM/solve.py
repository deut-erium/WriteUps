from Crypto.Util.number import long_to_bytes
from Crypto.Cipher import AES
import pwn
import hashlib
HOST, PORT = "crypto1.q21.ctfsecurinets.com", 1337

def decrypt(flag,secret):

    flag = bytes.fromhex(flag)
    iv,flag = flag[:16],flag[16:]
    key = hashlib.sha1(long_to_bytes(secret)).digest()[:16]
    return AES.new(key,AES.MODE_CBC,iv).decrypt(flag)



p = 169622824183424820825728324890204115101468714952998142585574034795946851153950475569207215681807529286667189170420372861538287664283023804761495759297626394111153684529019990561684722443184304549649494421130078368098045597169822975289983997491594344239614944483399038130689027660812095676588300142576532463429
p_minus_1 = str(p-1)

for _ in range(6):
    REM = pwn.remote(HOST,PORT)
    for i in range(6):
        REM.sendline(p_minus_1)
    enc_flag = REM.recvall().split()[-1].decode()
    if enc_flag.isalnum():
        print(decrypt(enc_flag,1))
        print(decrypt(enc_flag,p-1))
        break
    REM.close()

