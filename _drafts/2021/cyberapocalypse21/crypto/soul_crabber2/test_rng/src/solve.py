from pwn import xor
from tqdm import tqdm
x = b'418a5175c38caf8c1cafa92cde06539d512871605d06b2d01bbc1696f4ff487e9d46ba0b5aaf659807'
flag_enc = bytes.fromhex('418a5175c38caf8c1cafa92cde06539d512871605d06b2d01bbc1696f4ff487e9d46ba0b5aaf659807')

with open('dump.txt') as f:
    l = list(map(lambda x: x.strip(),f.readlines)))
    for t in tqdm(l):
        dec = xor(x,bytes.fromhex(t),flag_enc)
        if b'CHTB' in dec:
            print(dec)


#CHTB{cl4551c_ch4ll3ng3_r3wr1tt3n_1n_ru5t}
