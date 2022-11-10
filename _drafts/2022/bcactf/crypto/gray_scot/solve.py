import math
from Crypto.Util.Padding import pad
from Crypto.Util.number import bytes_to_long, long_to_bytes
from z3 import *


def chunks(l, n):
    assert(len(l) % n == 0)
    for i in range(0, len(l), n):
        yield l[i:i+n]

FLAG_LEN = 72
M_SIZE = math.isqrt(FLAG_LEN * 8)

def encrypt(ptxt,key):
    assert len(ptxt) == M_SIZE
    enc = [0] * M_SIZE
    for i in range(M_SIZE):
        for j in range(M_SIZE):
            if key[i][j] == 1:
                enc[i] ^= ptxt[j]
    return bytes(enc)

m = b'Reaction and diffusion of chemical species can produce a variety of patterns, reminiscent of those often seen in nature. The Gray Scott equations model such a reaction. For more information on this chemical system see the articles "Complex Patterns in a Simple System," by John E. Pearson and "Pattern Formation by Interacting Chemical Fronts," by K.J. Lee, W.D. McCormick, Qi Ouyang, and H.L. Swinney. These articles appeared in Science, Volume 261, 9 July 1993.'

messages = [i for i in chunks(pad(m, M_SIZE), M_SIZE)]

enc_m =  b'024274680e3f16196e3d43176b7d7f6e671a1833205372124f0e2c7c463e451c36365e19386a6323781e462231013f1b4c5625731d6204462375560e38737c7420105c6e6d0b6f4042553675122a570421654858283a637d7e5c1e747345370910056e2c176c060821284515337f3e2c74475f217309645d03497e1e072f20552d4c4809763777186e2550546a1f7b07491d7e751b2206513279125130667e246e4653667a046a42632e5d076274631a5d0638565f186b435675635274325c654a486c720b760d0d373f0b5661643430344f18723946750b1f4d316e4b7d00197d7a5a42392e747b310d587c6b543749293922174b1b3227477855587169782416594057051a17357f57371905045b787a556b3618083a436f327e1e556d25074b705c25740568765a6d326b415c793d0e2f773b497a365a60521b4403114d775744115f5f5e73387b35114d043371584958190e24456d5b4f21481c2c23547f5f31165b4832417b45612726415a5f25672d4e3a63732f586f4f26065965121e321f2547045d50126d19532e046c5440633437522b1567200a797947184b491f3d334f4a29017037176e443e0a2b6b5e561a03281e141f786052781d3f73081f2b48543d6e0860482e2e3f22063b242a170a062a00283b1d1724112231132a3b'

encs = [i for i in chunks(bytes.fromhex(enc_m.decode()), M_SIZE)]

key = [[Bool(f'k_{i}_{j}') for i in range(M_SIZE)] for j in range(M_SIZE)]


def encrypt_constraint(pt, ct):
    enc = [BitVecVal(0,8) for _ in range(M_SIZE)]
    for i in range(M_SIZE):
        for j in range(M_SIZE):
            enc[i] = If(key[i][j], enc[i]^pt[j], enc[i])
    return [i==j for i,j in zip(enc, ct)]

solver = Solver()
for pt,ct in zip(messages, encs):
    solver.add(encrypt_constraint(pt,ct))

keylist = []
for row in key:
    keylist.extend(row)


if solver.check() == sat:
    model = solver.model()
    key_flag = [[int(bool(model.eval(key[i][j]))) for j in range(M_SIZE) ] for i in range(M_SIZE)]
    flag_int = int("".join("".join(map(str,row)) for row in key_flag),2)
    print(long_to_bytes(flag_int))



