from pwn import *

LUT = [0, 4, 8, 12, 16, 20, 24, 28, 1, 5, 9, 13, 17, 21, 25, 29, 2, 6, 10, 14, 18, 22, 26, 30, 3, 7, 11, 15, 19, 23, 27,31]
SBOX = [32, 1, 82, 147, 4, 165, 198, 95, 56, 9, 138, 59, 12, 93, 142, 55, 8, 33, 42, 203, 100, 77, 230, 103, 136, 41, 162, 131, 44, 101, 46, 7, 176, 25, 114, 3, 28, 37, 30, 79, 0, 113, 98, 171, 20, 125, 118, 111, 40, 169, 26, 91, 196, 69, 150, 15, 48, 145, 18, 99, 156, 117, 166, 71, 16, 97, 90, 19, 140, 29, 78, 63, 160, 185, 74, 51, 148, 45, 126, 151, 88, 225, 170, 11, 84, 53, 22, 87, 224, 153, 218, 43, 52, 197, 94, 47, 168, 161, 34, 227, 76, 141, 174, 23, 128, 49, 154, 67, 60, 205, 70, 31, 120, 249, 66, 155, 236, 181, 62, 143, 152, 57, 2, 219, 36, 157, 54, 223, 112, 241, 146, 179, 68, 21, 6, 39, 72, 209, 122, 187, 252, 5, 214, 199, 144, 129, 130, 107, 180, 237, 246, 119, 24, 105, 106, 83, 220, 13, 158, 239, 104, 73, 250, 115, 164, 85, 110, 135, 208, 89, 50, 139, 108, 173, 14, 215, 184, 81, 234, 35, 92, 149, 238, 127, 64, 17, 178, 243, 228, 253, 86, 159, 240, 233, 226, 235, 116, 245, 102, 183, 232, 177, 194, 251, 124, 61, 190, 191, 216, 137, 58, 123, 132, 229, 134, 247, 192, 65, 210, 163, 172, 189, 38, 231, 200, 193, 10, 195, 244, 133, 222, 167, 96, 201, 186, 211, 204, 213, 182, 207, 80, 217, 202, 27, 188, 109, 206, 255, 248, 121, 242, 75, 212, 221, 254, 175]

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

def n2b(i):
    return [(i>>24)&0xff,(i>>16)&0xff,(i>>8)&0xff,i&0xff]
def b2n(i):
    return (i[0]<<24)|(i[1]<<16)|(i[2]<<8)|i[3]

assert b2n(n2b(0xdeadbeef)) == 0xdeadbeef

"""
print("P-Box:")
for i in range(32):
    x = 1 << i
    blocks = n2b(x)
    weird_shift(blocks)
    y = b2n(blocks)
    src,dst = len(bin(x)[3:]),len(bin(y)[3:])
    print(src%8,src//8,"=>",dst//4,dst%4)
"""

def encrypt_block(block, round_keys):
    out = block[:]

    for i in range(3):
        out = [a ^ b for a,b in zip(out, round_keys[i])]
        out = [SBOX[a] for a in out]
        weird_shift(out)

    out = [a ^ b for a,b in zip(out, round_keys[3])]
    out = [SBOX[a] for a in out]
    out = [a ^ b for a,b in zip(out, round_keys[4])]

    return out

def encrypt(data, round_keys, IV):
    num_blocks = len(data) // 4 # every 4 ints = 1 block

    encrypted = []

    # do initial block
    initial_block = [a^b for a,b in zip(data[:4], IV)]

    prev_enc = encrypt(initial_block, round_keys) # append encrypted data
    encrypted += prev_enc

    for i in range(1, num_blocks):
        prev_enc = encrypt_block([a^b for a,b in zip(data[4*i:4*i+4], prev_enc)], round_keys)
        encrypted += prev_enc
    return encrypted

round_keys = [
    [0,1,2,3],
    [4,5,6,7],
    [8,9,10,11],
    [12,13,14,15],
    [16,17,18,19]
]

data = [1,0,3,1]
print(hex(b2n(encrypt_block(data, round_keys)))[2:])

