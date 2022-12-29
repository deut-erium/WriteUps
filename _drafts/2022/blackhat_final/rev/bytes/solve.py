import pwn
from tqdm import tqdm
from collections import Counter, defaultdict
pwn.context.log_level = 100

with open("important.txt.enc.original","rb") as f:
    flag_enc = f.read()


def get_enc(text,filename="important.txt"):
    with open(filename,'wb') as f:
        f.write(text)
    p = pwn.process("./encryptor.exe "+filename,shell=True)
    p.wait()
    p.close()
    with open(filename+".enc","rb") as f:
        data=f.read()
    pwn.os.remove(filename+".enc")
    # pwn.os.remove(filename)
    return data

possible_encryptions = [defaultdict(set) for _ in range(443)]
possible_decryptions = [defaultdict(set) for _ in range(443)]

for i in tqdm(range(256)):
    for k in range(2):
        for _ in range(10):
            block = bytearray([i]*443)
            for t in range(443//9):
                block[9*t] = k
            enc = get_enc(block)
            for j,v in enumerate(enc):
                possible_encryptions[j][i].add(v)
                if j%9:
                    possible_decryptions[j][v].add(i)

for i,v in enumerate(flag_enc):
    print([chr(i) for i in possible_decryptions[i][v]])






