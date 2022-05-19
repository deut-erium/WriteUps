import random
from Crypto.Cipher import AES
from collections import Counter
from tqdm import tqdm
from z3 import *
import sys


def all_smt(s, initial_terms):
    def block_term(s, m, t):
        s.add(t != m.eval(t))

    def fix_term(s, m, t):
        s.add(t == m.eval(t))

    def all_smt_rec(terms):
        if sat == s.check():
            m = s.model()
            yield m
            for i in range(len(terms)):
                s.push()
                block_term(s, m, terms[i])
                for j in range(i):
                    fix_term(s, m, terms[j])
                yield from all_smt_rec(terms[i:])
                s.pop()
    yield from all_smt_rec(list(initial_terms))


with open('enc.bin', 'rb') as f:
    ciphertext = f.read()


def to_binary(b: bytes):
    return ''.join(['{:08b}'.format(c) for c in b])


def from_binary(s: str):
    return bytes(int(s[i:i + 8], 2) for i in range(0, len(s), 8))


def encrypt(key, message):
    return AES.new(key, AES.MODE_ECB).encrypt(message)


def decrypt(key: bytes, message: bytes):
    return AES.new(key, AES.MODE_ECB).decrypt(message)


def key_final_enc(key1, data):
    random.seed(key1)
    key_final = bytes(random.randrange(256) for _ in range(16))
    data_bits = list(to_binary(data))
    random.shuffle(data_bits)
    data = from_binary(''.join(data_bits))
    return encrypt(key_final, data)


def unshuffle(data_list, shuffle_order):
    res = [None] * len(data_list)
    for i, v in enumerate(shuffle_order):
        res[v] = data_list[i]
    return res


def test_unshuffle():
    random_text = list(random.randbytes(16 * 100))
    random_text_shuffled = random_text.copy()
    shuffle_order = list(range(len(random_text)))
    random.seed(10)
    random.shuffle(random_text_shuffled)
    random.seed(10)
    random.shuffle(shuffle_order)
    assert unshuffle(random_text_shuffled, shuffle_order) == random_text


test_unshuffle()


def key_final_dec(key1, ciphertext):
    random.seed(key1)
    key_final = bytes(random.randrange(256) for _ in range(16))

    data = decrypt(key_final, ciphertext)
    data_bits = list(to_binary(data))
    data_bits_order = list(range(len(data_bits)))
    random.shuffle(data_bits_order)
    data_bits_uns = unshuffle(data_bits, data_bits_order)
    data = from_binary(''.join(data_bits_uns))
    return data


def test_key_final_dec():
    random_text = random.randbytes(16 * 100)
    assert key_final_dec(10, key_final_enc(10, random_text)) == random_text


test_key_final_dec()

for key1 in tqdm(range(2**15), desc='solving for key1'):
    data = key_final_dec(key1, ciphertext)
    substitutions = Counter(data[i:i + 16] for i in range(0, len(data), 16))
    if len(substitutions) != len(data) // 16:
        print("pid =", key1)
        break

codes = list(''.join(chr(i) * 2 for i in range(0xb0, 0x1b0)))
random.seed(key1)
random.shuffle(codes)
sboxes = [''.join(codes[i * 4:(i + 1) * 4]).encode() for i in range(128)]
sbytes = b''.join(sboxes)
sboxints = list(map(lambda x: int.from_bytes(x, 'big'), set(
    sbytes[i:i + 2] for i in range(0, len(sbytes), 2))))
sboxes = [int.from_bytes(i, 'big') for i in sboxes]
data = key_final_dec(key1, ciphertext)
data_int = []
for i in range(0, len(data), 16):
    data_int.append(int.from_bytes(data[i:i + 16], 'big'))

flag = [BitVec('flag_' + str(i), 7) for i in range(len(data) // 64)]
sboxmap = Array('sbox', BitVecSort(7), BitVecSort(64))
aes_encryption = Function('AES', BitVecSort(16), BitVecSort(128))

constraints = [sboxmap[i] == sboxes[i] for i in range(128)]
for i in range(len(data) // 64):
    four_code = sboxmap[flag[i]]
    four_code_parts = [Extract(16 * i + 15, 16 * i, four_code)
                       for i in range(3, -1, -1)]
    for a, b in zip(data_int[4 * i:4 * i + 4], four_code_parts):
        constraints.append(aes_encryption(b) == a)
    constraints.append(Distinct([aes_encryption(i) for i in sboxints]))
solver = Solver()
solver.add(constraints)
# if solver.check() == sat:
# m = solver.model()
for m in all_smt(solver, flag):
    flag_bytes = bytes([m.eval(flag[i]).as_long() for i in range(len(flag))])
    assert len(set(flag_bytes)) == len(
        Counter(data[i:i + 64] for i in range(0, len(data), 64)))
    print(flag_bytes)
else:
    print("failed to solve")

# map_substitutions = {}
# for i,k in enumerate(substitutions.keys()):
#     map_substitutions[k] = CHARSET[i]

# substituted = bytes([map_substitutions[data[i:i+64]] for i in range(0,len(data),64)])
# print("try solving on quipquip?", substituted)
