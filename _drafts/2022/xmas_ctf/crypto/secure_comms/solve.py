from pwn import *
from z3 import *
import random

LUT = [0, 4, 8, 12, 16, 20, 24, 28, 1, 5, 9, 13, 17, 21, 25, 29, 2, 6, 10, 14, 18, 22, 26, 30, 3, 7, 11, 15, 19, 23, 27, 31]
SBOX_values = [32, 1, 82, 147, 4, 165, 198, 95, 56, 9, 138, 59, 12, 93, 142, 55, 8, 33, 42, 203, 100, 77, 230, 103, 136, 41, 162, 131, 44, 101, 46, 7, 176, 25, 114, 3, 28, 37, 30, 79, 0, 113, 98, 171, 20, 125, 118, 111, 40, 169, 26, 91, 196, 69, 150, 15, 48, 145, 18, 99, 156, 117, 166, 71, 16, 97, 90, 19, 140, 29, 78, 63, 160, 185, 74, 51, 148, 45, 126, 151, 88, 225, 170, 11, 84, 53, 22, 87, 224, 153, 218, 43, 52, 197, 94, 47, 168, 161, 34, 227, 76, 141, 174, 23, 128, 49, 154, 67, 60, 205, 70, 31, 120, 249, 66, 155, 236, 181, 62, 143, 152, 57, 2, 219, 36, 157, 54, 223, 112, 241, 146, 179, 68, 21, 6, 39, 72, 209, 122, 187, 252, 5, 214, 199, 144, 129, 130, 107, 180, 237, 246, 119, 24, 105, 106, 83, 220, 13, 158, 239, 104, 73, 250, 115, 164, 85, 110, 135, 208, 89, 50, 139, 108, 173, 14, 215, 184, 81, 234, 35, 92, 149, 238, 127, 64, 17, 178, 243, 228, 253, 86, 159, 240, 233, 226, 235, 116, 245, 102, 183, 232, 177, 194, 251, 124, 61, 190, 191, 216, 137, 58, 123, 132, 229, 134, 247, 192, 65, 210, 163, 172, 189, 38, 231, 200, 193, 10, 195, 244, 133, 222, 167, 96, 201, 186, 211, 204, 213, 182, 207, 80, 217, 202, 27, 188, 109, 206, 255, 248, 121, 242, 75, 212, 221, 254, 175]
SBOX = Array('SBOX', BitVecSort(8), BitVecSort(8))

def weird_shift_symbolic(block):
    # zero extend to 32 bits
    block = [ZeroExt(24, b) for b in block]

    v1 = 0
    for i in range(4):
        v1 |= block[i] << (8 * (3-i))

    # shift bits in v1
    v3 = 0
    for i in range(32):
        v3 |= (LShR(v1, i) & 1) << LUT[i]

    for i in range(4):
        block[3-i] = LShR(v3, (8*i)) & 0xff

    # truncate the values again
    block = [Extract(7, 0, b) for b in block]

    return block

def encrypt_block_symbolic(block, round_keys):
    out = block[:]

    for i in range(3):
        out = [a ^ b for a,b in zip(out, round_keys[i])]
        out = [(SBOX[a]&0xf8)|(a&7) for a in out]
        out = weird_shift_symbolic(out)
        out = [simplify(b) for b in out]

    out = [a ^ b for a,b in zip(out, round_keys[3])]
    out = [SBOX[a] for a in out]
    out = [a ^ b for a,b in zip(out, round_keys[4])]

    return out


def weird_shift(block):
    v1 = 0
    for i in range(4):
        v1 |= block[i] << (8 * (3-i))

    # shift bits in v1
    v3 = 0
    for i in range(32):
        v3 |= ((v1 >> i) & 1) << LUT[i]

    # store back into block (by reference)
    for i in range(4):
        block[3-i] = (v3 >> (8*i)) & 0xff

def unshift(block):
    v1 = 0
    for i in range(4):
        v1 |= block[i] << (8 * (3-i))

    # shift bits in v1
    v3 = 0
    for i in range(32):
        v3 |= ((v1 >> LUT[i]) & 1) << i

    # store back into block (by reference)
    for i in range(4):
        block[3-i] = (v3 >> (8*i)) & 0xff

def encrypt_block(block, round_keys):
    out = block[:]

    for i in range(3):
        out = [a ^ b for a,b in zip(out, round_keys[i])]
        out = [SBOX_values[a] for a in out]
        weird_shift(out)

    out = [a ^ b for a,b in zip(out, round_keys[3])]
    out = [SBOX_values[a] for a in out]
    out = [a ^ b for a,b in zip(out, round_keys[4])]

    return out

INV_SBOX = {SBOX_values[i]:i for i in range(256)}
def decrypt_block(block, round_keys):
    out = block[:]
    out = [a ^ b for a,b in zip(out, round_keys[4])]
    out = [INV_SBOX[a] for a in out]
    out = [a ^ b for a,b in zip(out, round_keys[3])]

    for i in range(2,-1,-1):
        unshift(out)
        out = [INV_SBOX[a] for a in out]
        out = [a ^ b for a,b in zip(out, round_keys[i])]

    return out

def dec(data_blocks, iv, round_keys):
    prev_enc = data_blocks[:4]
    first_dec = decrypt_block(prev_enc, round_keys)
    first_dec = [a^b for a,b in zip(first_dec, iv)] # first block has iv xored in
    t = first_dec
    for i in range(1, len(data_blocks) // 4):
        block = data_blocks[4*i:4*i+4]
        cur_dec = decrypt_block(block, round_keys)
        cur_dec = [a^b for a,b in zip(cur_dec, prev_enc)] # xor with the previous encrypted block
        prev_enc = data_blocks[4*i:4*i+4]
        t += cur_dec
    return t

def enc(data_blocks, iv, round_keys):
    block = [a^b for a,b in zip(data_blocks[:4], iv)]
    t = encrypt_block(block, round_keys)

    for i in range(1, len(data_blocks) // 4):
        block = [a^b for a,b in zip(t[-4:], data_blocks[4*i:4*i+4])]
        t += encrypt_block(block, round_keys)
    return t



round_keys = [
    [11,2,3,4],
    [2,3,4,5],
    [3,4,5,6],
    [4,5,123,7],
    [5,6,37,8]
]


data = list(range(120))
iv = [1,2,3,4]
print(dec(enc(data, iv, round_keys), iv, round_keys), data)
assert dec(enc(data, iv, round_keys), iv, round_keys) == data

def n2b(i):
    return [(i>>24)&0xff,(i>>16)&0xff,(i>>8)&0xff,i&0xff]
def b2n(i):
    return (i[0]<<24)|(i[1]<<16)|(i[2]<<8)|i[3]

assert decrypt_block(encrypt_block([1,2,3,4], round_keys), round_keys) == [1,2,3,4]

r = remote("challs.htsp.ro", 10001)
#r = process("./securecomms(1)")

CNT = 32
print("Creating data...")
datas = [[random.randint(0, 255) for _ in range(4)] for _ in range(CNT)]
encs = []
for i in range(CNT):
    r.sendlineafter(b"cmd =", b"1")
    r.sendlineafter(b"pt =", bytes(datas[i]).hex().encode())
    r.recvuntil(b"ct = ")
    x = list(bytes.fromhex(r.recvline().decode()))
    encs.append(x)

s = Solver()
rkeys = [[BitVec(f"rkey_{i}_{j}", 8) for j in range(4)] for i in range(5)]

for i,v in enumerate(SBOX_values):
    print(f"Adding Sbox {i}/256 => {v}")
    s.add(SBOX[i] == v)

for i in range(CNT):
    print(f"Adding result {i}/{CNT}")
    enc_block = encrypt_block_symbolic(datas[i], rkeys)
    for j in range(4):
        s.add(enc_block[j] == encs[i][j])

while s.check() == sat:
    m = s.model()
    test_rkey = [[m[rkeys[i][j]].as_long() for j in range(4)] for i in range(5)]
    v = []
    for i in range(5):
        for j in range(4):
            v.append(test_rkey[i][j] != rkeys[i][j])
    s.add(Or(*v))

    print(test_rkey)

    r.sendlineafter(b"cmd =", b"2")
    r.recvuntil(b"iv = ")
    iv = list(bytes.fromhex(r.recvline().decode()))
    r.recvuntil(b"ct = ")
    ct = list(bytes.fromhex(r.recvline().decode()))
    pt = bytes(dec(ct, iv, test_rkey)).hex()
    r.sendlineafter(b"pt = ", pt.encode())
    r.interactive()

else:
    print("Nope :(")
