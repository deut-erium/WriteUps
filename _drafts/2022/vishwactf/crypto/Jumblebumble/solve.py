from math import gcd
from itertools import combinations
import gmpy2

with open("JumbleBumble.txt") as f:
    necs = list(map(lambda x: [int(i) for i in x.split()], f.read().strip().split("\n\n")))


# ns = [i[0] for i in necs]
# factors = set()
# for a, b in combinations(ns, 2):
#     if (x := gcd(a, b)) != 1:
#         factors.update({x, a//x, b//x})

cs = [i[-1] for i in necs]
for c in cs:
    root, is_root = gmpy2.iroot(c, 4)
    if is_root:
        root = int(root)
        root_bytes = root.to_bytes((root.bit_length() + 7)//8, 'big')
        print(root_bytes)
