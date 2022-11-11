import pwn
from tqdm import tqdm

def long_to_bytes(x):
    return int.to_bytes(x,(x.bit_length()+7)//8,'big')

enc_flag = long_to_bytes(2692665569775536810618960607010822800159298089096272924)

def encrypt(x:bytes)->int:
    pwn.context(log_level=100)
    with open('flag.txt','wb') as f:
        f.write(x)
    p = pwn.process('pypy3 chall.py',shell=True)
    data = p.recvline()
    p.close()
    return long_to_bytes(int(data))
    #return int(data)

flag = b''
for i in range(len(flag),len(enc_flag)):
    for j in tqdm(range(1,128)[::-1]):
        if encrypt(flag+bytes([j]))[i]==enc_flag[i]:
            flag+=bytes([j])
            print(flag)
            break

#actf{3p1c_0n3_l1n3r_95}
