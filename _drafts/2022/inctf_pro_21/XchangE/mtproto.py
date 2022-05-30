from Crypto.Util.number import bytes_to_long, inverse, long_to_bytes
from Crypto.Random import get_random_bytes
from Crypto.Random.random import randint
from Crypto.Protocol.KDF import scrypt
from secret import FLAG, FAKEFLAG
import hashlib, binascii

P = (1 << 1024) - 1093337
G = 7
IV = b"y3ll0w subm4r1n3"

class PublicKey:

    def __init__(self, h, p, g, q):
        self.h = h
        self.p = p
        self.g = g
        self.q = q

class PrivateKey:

    def __init__(self, x, p, g, q):
        self.x = x
        self.p = p
        self.g = g
        self.q = q

def generate_key():

    p = P
    x = randint(2, p-2)
    g = G
    q = p - 1
    h = pow(g, x, p)

    pubkey = PublicKey(h, p, g, q)
    privkey = PrivateKey(x, p, g, q)

    return (pubkey, privkey)

def kdf(secret):

    password = long_to_bytes(secret)
    salt = IV
    pswd = scrypt(password, salt, 16, N=2**14, r=8, p=1)

    key = binascii.hexlify(pswd[:16])

    return str(key)

if __name__ == "__main__":

    print("(p,g) = ({0},{1})\n".format(P,G))

    pub_alice, priv_alice = generate_key()
    print("Message from alice:",pub_alice.h)

    print("\nsend to Bob->")
    T_alice = int(input())

    pub_bob, priv_bob = generate_key()
    print("\nMessage from bob:",pub_bob.h)

    print("\nsend to Alice->")
    T_bob = int(input())

    y = randint(2, P-2)
    pub, priv = generate_key()

    nonce_alice = pow(pub.h, priv.x*y,P)

    print("\nnonce send to Alice:", nonce_alice)

    print("\nsend nonce value to Bob->")
    nonce_bob = int(input())

    secret_bob =  pow(T_alice, priv_bob.x, P) ^  nonce_bob
    secret_alice = pow(T_bob, priv_alice.x,P) ^ nonce_alice

    if secret_bob == 0 or secret_alice == 0 or T_alice == 0 or T_bob == 0 or T_alice == 1 or T_bob == 1:
        print("sorry cant do!!")
        exit()

    assert secret_bob == secret_alice , b"you messed up"

    key = kdf(secret_alice)

    print("\nsend s->")
    s = input()

    if s == key :
        print(FLAG)

    else:
        print(FAKEFLAG)
    print(key)
    print(s)
