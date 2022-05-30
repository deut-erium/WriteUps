from zlib import crc32
import string
from itertools import product
from tqdm import tqdm

CHARSET = (string.ascii_letters + string.digits).encode()

target = b"the"

prefix = b"Screw Sekai"

target_crc = crc32(target)
for b in tqdm(product(CHARSET,repeat=6),total=len(CHARSET)**6):
    if target_crc == crc32(prefix+bytes(b)):
        result = prefix+bytes(b)
        print(result, crc32(target), crc32(result), target)
        break

# b'Screw Sekaidh0CLP' 1011183078 1011183078 b'the'
