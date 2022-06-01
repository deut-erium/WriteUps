from base64 import b64decode as decode
from itertools import product

data = 'zmxhz3tkb2vzx3roaxnfzxzlbl9jb3vudf9hc19jcnlwdg9vb30='
CHARSET = 'abcdefghijklmnopqrstuvwxyz_{}'


def case_variations(string):
    possibilities = []
    for char in string:
        possibilities.append([char.lower(), char.upper()])
    return ["".join(perm) for perm in product(*possibilities)]


flag = b""
real_data = ""
for i in range(0, len(data), 4):
    crib = data[i:i + 4]
    for case_variation in case_variations(crib):
        if all(chr(char) in CHARSET for char in decode(case_variation)):
            real_data += case_variation
            flag += decode(case_variation)
            print(flag)
            break

print(real_data)
