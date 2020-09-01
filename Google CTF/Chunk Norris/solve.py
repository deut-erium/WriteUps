from functools import reduce
from itertools import chain, combinations
from operator import mul
import gmpy2
from Crypto.Util.number import *

n = 0xab802dca026b18251449baece42ba2162bf1f8f5dda60da5f8baef3e5dd49d155c1701a21c2bd5dfee142fd3a240f429878c8d4402f5c4c7f4bc630c74a4d263db3674669a18c9a7f5018c2f32cb4732acf448c95de86fcd6f312287cebff378125f12458932722ca2f1a891f319ec672da65ea03d0e74e7b601a04435598e2994423362ec605ef5968456970cb367f6b6e55f9d713d82f89aca0b633e7643ddb0ec263dc29f0946cfc28ccbf8e65c2da1b67b18a3fbc8cee3305a25841dfa31990f9aab219c85a2149e51dff2ab7e0989a50d988ca9ccdce34892eb27686fa985f96061620e6902e42bdd00d2768b14a9eb39b3feee51e80273d3d4255f6b19
e = 0x10001
c = 0x6a12d56e26e460f456102c83c68b5cf355b2e57d5b176b32658d07619ce8e542d927bbea12fb8f90d7a1922fe68077af0f3794bfd26e7d560031c7c9238198685ad9ef1ac1966da39936b33c7bb00bdb13bec27b23f87028e99fdea0fbee4df721fd487d491e9d3087e986a79106f9d6f5431522270200c5d545d19df446dee6baa3051be6332ad7e4e6f44260b1594ec8a588c0450bcc8f23abb0121bcabf7551fd0ec11cd61c55ea89ae5d9bcc91f46b39d84f808562a42bb87a8854373b234e71fe6688021672c271c22aad0887304f7dd2b5f77136271a571591c48f438e6f1c08ed65d0088da562e0d8ae2dadd1234e72a40141429f5746d2d41452d916

a = 0xe64a5f84e2762be5
chunk_size = 64

z = gmpy2.invert(a, 1 << 64)
v = pow(z, 15, 1 << 64)


def check(x):
    if (x < (1 << 64)):
        q = (x * v) % (1 << 64)
        if (q & 0xc000000000000001 == 0xc000000000000001) and (gen_prime(q) is not None):
            return True


def sanitize(l):
    z = []
    for p, q in l:
        if (check(p) is not None) and (check(q) is not None):
            if (p > q):
                p, q = q, p
            z.append((p, q))
    return z


def gen_prime(s):
    s |= 0xc000000000000001
    p = 0
    for _ in range(1024 // chunk_size):
        p = (p << chunk_size) + s
        s = a * s % 2**chunk_size
    if gmpy2.is_prime(p):
        return p


M = n % (1 << 64)
N = (n // (1 << 64)) % (1 << 64)
lo = M
hi = (N-2*z*lo) % (1 << 64)

F = (hi << 64)+lo
print(F)
# factors
fac = [11, 13, 109, 223, 1290533, 4608287, 167541865434116759]

t = [reduce(mul, x, 1) for x in (chain.from_iterable(combinations(fac, r)
                                                     for r in range((len(fac)) + 1)))]
t = [(i, int(F)//i) for i in t]
print(set(sanitize(t)))
# {(1590130175551765067, 2178044250643517867)}
S_1 = (1590130175551765067 * v) % (1 << 64)
S_2 = (2178044250643517867 * v) % (1 << 64)

p = gen_prime(S_1)
q = gen_prime(S_2)

assert(p*q == n)
print(long_to_bytes(pow(c, int(gmpy2.invert(e, (p-1)*(q-1))), n)))
