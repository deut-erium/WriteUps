# import pwn
# pwn.context(log_level=1000)
# from tqdm import tqdm
# for i in tqdm(range(10**9)):
#     sent = "3\n"+",".join(list(str(i).zfill(9)))
#     p = pwn.process('./mountains_and_masterpiece')
#     p.sendline(sent)
#     data = p.recvall()
#     if b'Incorrect' not in data:
#         print(data)
#         break
#     p.close()

MAT = [0xa, 0x1f, 0x1a, 0x28, 0x13, 0x14, 0x24, 0x27, 0xd, 0xc, 0x2, 0x1e,
        0x1e, 0x1b, 0x14, 0x21, 0x2, 0x1b, 0x24, 0x17, 0xa, 0x16, 0x12, 0x12,
        0x5, 0x24, 0xd, 0x27, 0x14, 0x1b, 0x23, 0x6, 0x23]

FIRST_ARR = [73, 36, 52, 57, 84, 69, 52, 78, 125, 35, 51, 89, 53, 35, 90, 76, 90, 71, 65, 52, 88, 82, 72, 88, 123, 84, 88, 76, 73, 65, 123, 76, 51, 95, 68, 90, 56, 49, 125, 82, 66]
SECOND_ARR = [95, 68, 90, 56, 49, 125, 82, 66, 83, 70, 73, 50, 57, 123, 87, 77, 80, 67, 65, 53, 88, 54, 78, 71, 79, 48, 72, 76, 81, 55, 84, 89, 74, 69, 85, 51, 52, 86, 75, 35, 36]



# MAT = [ 0xa , 0x1f, 0x1a,                   [ o1 ,o2, o3
#         0x28, 0x13, 0x14,                     o4 ,o5, o6
#         0x24, 0x27, 0xd,                      o7 ,o8, o9
#         0xc , 0x2 , 0x1e,      [a, d, g]      o4
#         0x1e, 0x1b, 0x14,   X  [b, e, h]  =   o5
#         0x21, 0x2 , 0x1b,      [c, f, i]      o6
#         0x24, 0x17, 0xa,                      o7
#         0x16, 0x12, 0x12,                     o8
#         0x5 , 0x24, 0xd,                      o9
#         0x27, 0x14, 0x1b,                     o10
#         0x23, 0x6 , 0x23]                     o11 ,o22, o32]

# [a,b,c] m0,m3           ]   [o1, o1, o2, o10,         o11]
# [d,e,f] m1,m4           ] = [o12, o5                   o22]
# [g,h,i] m2,m5 ....      ]   [o3, o6                   o33]



# MAT*inp = outputT

def enc(inp):
    final_chars = [0]*33
    for i in range(11):
        for j in range(3):
            res = sum(x*y for x,y in zip(inp[3*j:3*j+3],MAT[3*i:3*i+3]))
            res%=41
            final_chars[i+11*j] = SECOND_ARR[res]
    return final_chars
            

indices_req = [SECOND_ARR.index(i) for i in b'VULNCON{#41_UP51D3_D0WN_S#0W3L5}']

from itertools import product
rrr = 8
for bzz in product(range(41),repeat=3):
    tts = [sum(x*y for x,y in zip(bzz,MAT[3*i:3*i+3]))%41 for i in range(rrr)]
    if tts==indices_req[:rrr]:
        print(bzz)

rrr = 4
for bzz in product(range(41),repeat=3):
    tts = [sum(x*y for x,y in zip(bzz,MAT[3*i:3*i+3]))%41 for i in range(rrr)]
    if tts==indices_req[-rrr:]:
        print(bzz)

