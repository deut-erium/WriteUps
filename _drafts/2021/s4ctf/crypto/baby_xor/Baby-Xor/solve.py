with open('flag.enc','rb') as f:
    flag_enc = f.read()

def xor(a,b):
    return bytes([i^j for i,j in zip(a,b)])

for initial in range(256):
    flag = bytearray(len(flag_enc))
    flag[0] = initial
    for i in range(1,len(flag)):
        flag[i] = flag[i-1]^flag_enc[i]
    if b'S4CTF' in flag:
        print(flag)

#S4CTF{XOR_x0r_XoR_X0r_xOr!!!}
