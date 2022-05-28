import json
import string
from collections import Counter
from random import randbytes
from tqdm import tqdm
from pwn import remote, re
from itertools import product

# HOST, PORT = "localhost", "1337"
# HOST, PORT = "46.101.27.51", 30002
HOST, PORT = "165.22.124.40",32260
REM = remote(HOST, PORT)
REM.recvuntil(b'>')

def xor(a,b):
    return bytes([i^j for i,j in zip(a,b)])

def check_iv(iv:bytes):
    payload = {"option":"encrypt"}
    payload["iv"] = iv.hex()
    payload["pt"] = "00"
    REM.sendline(json.dumps(payload))
    data = REM.recvuntil(b'>')
    response = json.loads(re.search(b"(\{.*\})", data)[0])
    return bytes.fromhex(response['ct'])

def try_claiming(key:bytes):
    payload = {"option":"claim"}
    payload["key"] = key.hex()
    REM.sendline(json.dumps(payload))
    data = REM.recvuntil(b'>')
    response = json.loads(re.search(b"(\{.*\})", data)[0])
    if response['response'] == 'success':
        print(response['flag'])
        return response['flag']



def ksa(key,pos):
    S = list(range(256))
    j = 0
    for i in range(pos):
        j = (j + S[i] + key[i%len(key)]) % 256
        S[i],S[j] = S[j],S[i]
    return S,j

key_bytes = b''
FLAG_LEN = 27
while len(key_bytes)<FLAG_LEN:
    target = (len(key_bytes) - FLAG_LEN)%256
    freq = Counter()
    for i in tqdm(range(50)):
        nonce = bytes([0, target-1]) + randbytes(256-FLAG_LEN -2)
        O = check_iv(nonce)[0]
        S,j = ksa(nonce+key_bytes,len(nonce+key_bytes))
        if S[1]!=target:
            continue
        T = {s:i for i,s in enumerate(S)}
        freq[ (T[ (T[O] - target)%256] - j - S[target])%256]+=1
    print(freq)
    key_bytes+=bytes([freq.most_common()[0][0]])
    print(key_bytes)


flag = try_claiming(key_bytes)
print(flag)
# HTB{f1uhr3r_m4n71n_p1u5_5h4m1r_15_4_cl4ss1c_0n3!!!}



