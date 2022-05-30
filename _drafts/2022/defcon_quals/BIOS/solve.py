import lzma
from pwn import xor

HEADERS = [
        "5d 00 00 01 00",
        "5d 00 00 10 00",
        "5d 00 00 08 00",
        "5d 00 00 10 00",
        "5d 00 00 20 00",
        "5d 00 00 40 00",
        "5d 00 00 80 00",
        "5d 00 00 00 01",
        "5d 00 00 00 02"
        ]

HEADERS = list(map(bytes.fromhex,HEADERS))


with open("flag.lzma.enc","rb") as f:
    flag_enc = f.read()

for h in HEADERS:
    k = xor(h,flag_enc[:5])
    flzma = xor(k,flag_enc)
    try:
        print(lzma.decompress(flzma))
    except:
        continue
