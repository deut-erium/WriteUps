import pwn
import re
HOST,PORT = "challs.dvc.tf", 3333
REM = pwn.remote(HOST,PORT)
pwn.context(log_level=0)
REM.recvuntil(b'encrypt?')



def encrypt(pt:bytes):
    REM.sendline(pt.hex())
    data = REM.recvuntil(b'encrypt?')
    #print(data)
    flip = b'!' in data
    enc = bytes.fromhex(re.search(b' ([a-f0-9]+)\n',data)[1].decode())
    if flip:
        return pwn.xor(enc,b'\xff')
    return enc

def encrypt_big(data):
    MAX_SIZE = 0x10*56
    for i in range((len(data)-1)//MAX_SIZE+1):
        block = data[i*MAX_SIZE:(i+1)*MAX_SIZE]
        ct = encrypt(block)[:len(block)]
        for j in range(len(ct)//0x10):
            yield ct[j*0x10:(j+1)*0x10]

charset = list(b"etoanihsrdlucgwyfmpbkvjxqz{}_01234567890ETOANIHSRDLUCGWYFMPBKVJXQZ")
for i in range(0x100):
    if i not in charset:
        charset.append(i)

targets = [encrypt(b"A"*(0x10-i)) for i in range(0x10)]

lengths = list(map(len, targets))
flag_len = lengths[-1] - 0x11 + lengths.index(lengths[-1])

flag = b""
for _ in range(flag_len):
    print(flag)
    b, i = divmod(len(flag) + 1, 0x10)
    target = targets[i][b*0x10:(b+1)*0x10] # get the ciphertext of that block
    attempts = b""
    for c in charset:
        attempts += (b"A"*0x10+flag+bytes([c]))[-0x10:]
        for c, ct in zip(charset, encrypt_big(attempts)):
            if ct == target:
                flag += bytes([c])
                print(flag)
                break
            else:
                print("oof")
print(f"solved in {rcount} HTTP requests!")
