import string
import random
import os
import re
from pwn import remote

HOST, PORT = "challs.actf.co", 31333

REM = remote(HOST, PORT)


alpha = string.ascii_lowercase
inner = alpha+"_"
noise = inner + "{}"

def encrypt(msg, key):
    ret = ""
    i = 0
    for c in msg:
        if c in alpha:
            ret += alpha[(alpha.index(key[i]) + alpha.index(c)) % len(alpha)]
            i = (i + 1) % len(key)
        else:
            ret += c
    return ret

def decrypt(msg, key):
    inv_key = "".join(alpha[-alpha.index(i)] for i in key)
    return encrypt(msg, inv_key)


def decrypt_challenge(msg):
    for poss_fleg, poss_keye in re.findall("\{([a-z_]{10,50})\}([a-z]{4})", msg):
        poss_key = decrypt(poss_keye, 'fleg')
        # print(poss_fleg, poss_keye, poss_key)
        for i in range(4):
            key = poss_key[i:] + poss_key[:i]
            decrypted = decrypt(msg, key)
            if "actf{" in decrypted:
                return re.findall("actf\{[a-z_]{10,50}\}", decrypted)[0]


for _ in range(50):
    chall_data = REM.recvuntil(">")
    chall_data = chall_data.split(b": ")[1].split()[0].decode()
    # key = decrypt(chall_data[-4:],'fleg')
    REM.sendline(decrypt_challenge(chall_data))

# actf{classical_crypto_is_not_the_best}
