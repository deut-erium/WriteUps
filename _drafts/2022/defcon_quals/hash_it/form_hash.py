import hashlib

from itertools import product
from collections import defaultdict

invmap = {
        "md5":defaultdict(list),
        "sha1":defaultdict(list),
        "sha256":defaultdict(list),
        "sha512":defaultdict(list)
        }

for hashname, mapset in invmap.items():
    for word in product(range(1,256),repeat=2):
        first_byte = hashlib.new(hashname,bytes(word)).digest()[0]
        mapset[first_byte].append(bytes(word))


def reverse_shellcode(shell, hashname):
    res = []
    for b in shell:
        res.append(invmap[hashname][b][0])
    return b"".join(res)

x = "5d 00 00 00 08 00 44 94 a6 b1 a9 14 37 65 03 e8 61 4e b5 0a 29 f7 bc f4 0a 39 10 76 ec 9c fe 41 1a 6a 07 81 ce e1 e0 58 3f 2f a1 6a c9 03 2d 24 38 74 b0 3d 19 ab 33 0c 73 57 75 94 da 8a ac 7e"
