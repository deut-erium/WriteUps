
from cryptography.hazmat.primitives.ciphers import (
        Cipher, algorithms, modes
    )
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.exceptions import InvalidTag
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from bitstring import BitArray, Bits


def check_correctness(keyset, nonce, ct):
    flag = True
    for i in range(len(keyset)):
        aesgcm = AESGCM(key)
        try:
            aesgcm.decrypt(nonce, ct, None)
        except InvalidTag:
            flag = False
    assert flag

def bytes_to_element(val, field, a):
    bits = BitArray(val)
    result = field.fetch_int(0)
    for i in range(len(bits)):
        if bits[i]:
            result += a^i
    return result

P.<x> = PolynomialRing(GF(2))
p = x^128 + x^7 + x^2 + x + 1
GFghash.<a> = GF(2^128,'x',modulus=p)
R = PolynomialRing(GFghash, 'x')

def multi_collide_gcm(keyset, nonce=b'\x00'*12, tag=b'\x01'*16):
    # encode length as lens
    lens_byte = int(len(keyset)*128).to_bytes(16,'big')
    lens_bf = bytes_to_element(lens_byte, GFghash, a)
    # increment nonce
    nonce_plus = nonce+bytes([0,0,0,1])
    # encode fixed ciphertext block and tag
    tag_bf = bytes_to_element(tag, GFghash, a)
    pairs = []
    for k in keyset:
        # compute H
        aes = AES.new(k, AES.MODE_ECB)
        H = aes.encrypt(b'\x00'*16)
        h_bf = bytes_to_element(H, GFghash, a)
        # compute P
        P = aes.encrypt(nonce_plus)
        p_bf = bytes_to_element(P, GFghash, a)
        # assign (lens * H) + P + T to b
        b = (lens_bf * h_bf) + p_bf + tag_bf

        # get pair (H, b*(H^-2))
        y =  b * h_bf^-2
        pairs.append((h_bf, y))

    # compute Lagrange interpolation
    f = R.lagrange_polynomial(pairs)
    ct = ''
    for coeff in f.list()[::-1]:
        ct_pad = ''.join(map(str,coeff.polynomial().list()))
        ct += Bits(bin=ct_pad.ljust(128,'0'))
    ct = ct.bytes
    return ct+tag


n = int(input())
keyset = []
for i in range(n):
    key = get_random_bytes(16)
    keyset.append(key)
    continue
    t = input()
    keyset.append(bytes.fromhex(t))

ct = multi_collide_gcm(keyset)
print(ct.hex())
check_correctness(keyset, b'\x00'*12, ct)









