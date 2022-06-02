import random
import string
import time

from base64 import b64encode, b64decode
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from Crypto.Cipher import AES
from itertools import product
from bitstring import BitArray, Bits
import pwn

derived_keys = []  # keys derived from scrypt of password
rev_keys = {}  # holds mapping from derived key to password
for k in product(string.ascii_lowercase, repeat=3):
    kdf = Scrypt(salt=b'', length=16, n=16, r=8,
                 p=1, backend=default_backend())
    derived_key = kdf.derive("".join(k).encode())
    derived_keys.append(derived_key)
    rev_keys[derived_key] = "".join(k)

HOST, PORT = "pythia.2021.ctfcompetition.com", 1337
REM = pwn.remote(HOST, PORT)


def bytes_to_element(val, field, a):
    bits = BitArray(val)
    result = field.fetch_int(0)
    for i in range(len(bits)):
        if bits[i]:
            result += a**i
    return result


P.<x> = PolynomialRing(GF(2))
p = x**128 + x**7 + x**2 + x + 1
GFghash.<a> = GF(2**128, 'x', modulus=p)
R = PolynomialRing(GFghash, 'x')


def multicollision(keyset, nonce=b'\x00' * 12, tag=b'\x01' * 16):
    L_bytes = int(len(keyset) * 128).to_bytes(16, 'big')
    L_bf = bytes_to_element(L_bytes, GFghash, a)
    nonce_plus = nonce + bytes([0, 0, 0, 1])
    tag_bf = bytes_to_element(tag, GFghash, a)
    pairs = []
    for k in keyset:
        # compute H
        aes = AES.new(k, AES.MODE_ECB)
        H = aes.encrypt(b'\x00' * 16)
        h_bf = bytes_to_element(H, GFghash, a)

        s = aes.encrypt(nonce_plus)
        s_bf = bytes_to_element(s, GFghash, a)
        # assign (lens * H) + s + T to b
        b = (L_bf * h_bf) + s_bf + tag_bf
        # get pair (H, b*(H^-2))
        y = b * h_bf**-2
        pairs.append((h_bf, y))
    # compute Lagrange interpolation
    f = R.lagrange_polynomial(pairs)
    ct = ''
    for coeff in f.list()[::-1]:
        ct_pad = ''.join(map(str, coeff.polynomial().list()))
        ct += Bits(bin=ct_pad.ljust(128, '0'))
    ct = ct.bytes
    return ct + tag


def decrypt_text(text):
    REM.sendline(b'3')
    REM.sendline('A' * 16 + ',' + pwn.b64e(text))
    data = REM.recvuntil(b'Exit\n>>> ')
    return b'successful' in data


def search(size=367):
    start_time = time.time()
    api_count = 0
    for i in range(0, 26**3, size):
        print("trying range ({},{})".format(i, i + size))
        api_count += 1
        if decrypt_text(multicollision(derived_keys[i:i + size])):
            print(i, i + size)
            break
    lo, hi = i, i + size
    while lo <= hi:
        mid = (lo + hi) // 2
        api_count += 1
        print("trying range ({},{})".format(lo, hi))
        if decrypt_text(multicollision(derived_keys[lo:mid + 1])):
            hi = mid - 1
        else:
            lo = mid + 1
    if decrypt_text(multicollision(derived_keys[lo:lo + 1])):
        keyindex = lo
    else:
        keyindex = lo + 1
    password = rev_keys[derived_keys[keyindex]]
    print("key:{} found in {} calls".format(password, api_count))
    print("time taken :", time.time() - start_time)
    return password


REM.recvuntil(b'Exit\n>>>')
password = ""
for key_index in range(3):
    REM.sendline(b'1')  # option1
    REM.sendline(str(key_index))
    REM.recvuntil(b'Exit\n>>>')
    password += search()


REM.sendline(b'2')
REM.sendline(password)
print(REM.recvall())
# CTF{gCm_1s_n0t_v3ry_r0bust_4nd_1_sh0uld_us3_s0m3th1ng_els3_h3r3}
