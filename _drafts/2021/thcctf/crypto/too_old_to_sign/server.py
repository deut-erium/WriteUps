#!/usr/local/bin/python3.8

from Crypto.PublicKey import RSA
from Crypto.Util.number import long_to_bytes, bytes_to_long
from secret import FLAG, aes_key
from hashlib import sha1
from os import urandom


def sign1(sk, m):
    mq, dq = m % sk.q, sk.d % (sk.q - 1)
    mp, dp = m % sk.p, sk.d % (sk.p - 1)
    s1 = pow(mq, dp, sk.q)
    s2 = pow(mp, dp, sk.p)
    h = (sk.u * (s1 - s2)) % sk.q
    s = (s2 + h * sk.p) % sk.n
    return s


def sign2(sk, m):
    mq, dq = m % sk.q, sk.d % (sk.q - 1)
    mp, dp = m % sk.p, sk.d % (sk.p - 1)
    s1 = pow(mq, dq, sk.q)
    s2 = pow(mp, dq, sk.p)
    h = (sk.u * (s1 - s2)) % sk.q
    s = (s2 + h * sk.p) % sk.n
    return s


def pad(m, n):
    return m + urandom(n // 8)


def encode(m, n):
    return b"\x6a" + m[:(n - 160 - 16) // 8] + sha1(m).digest() + b"\xbc"


assert(len(aes_key) == 16)

private_key = RSA.generate(2048)

message = b"Here is a message to inform you that this AES key : -" + aes_key + \
    b"- will allow you to decrypt my very secret message. I signed my message to prove my good faith, but make sure no one is watching...\n"
message += b"An anonymous vigilante trying to preserve Thcon and our delicious cassoulet"


padded_message = pad(message, 2048)
encoded_message = encode(padded_message, 2048)

signature1 = sign1(private_key, bytes_to_long(encoded_message))
print("signature1 =", signature1)
signature2 = sign2(private_key, bytes_to_long(encoded_message))
print("signature2 =", signature2)
print("e =", private_key.e)
print("n =", private_key.n)

pt = bytes_to_long(FLAG)
print("ct =", pow(pt, private_key.e, private_key.n))

d = private_key.d
dp = private_key.d%(private_key.p-1)
dq = private_key.d%(private_key.q-1)
m = bytes_to_long(encoded_message)
p = private_key.p
q = private_key.q
n = private_key.n
e = 65537
segment_1 = encoded_message[:54]
segment_2 = encoded_message[70:-20]
seg1 = bytes_to_long(segment_1)
seg2 = bytes_to_long(segment_2)
v1 = pow(signature1,e,n)
v2 = pow(signature2,e,n)
m1 = seg1*2**1616+ seg2*2**160


#from math import gcd
#from z3 import *
##k1,k2,pp,qq,mm,key,hsh = Ints('k1 k2 pp qq mm key hsh')
#k1,k2,pp,qq,mm = [BitVec(i,2048) for i in 'k1 k2 pp qq mm'.split()]
#key = BitVec('key',128)
#hsh = BitVec('hsh',160)
#solver = Solver()
#solver.add(k1*pp+mm==v1)
#solver.add(k2*qq+mm==v2)
#


#solver.add(pp*qq==n)
#solver.add(mm==hsh+2**160*seg2+2**1488*key+2**1616*seg1)

#solver.add(
#solver.add([hsh>2**159,key>2**127,pp>1,qq>1])
#





