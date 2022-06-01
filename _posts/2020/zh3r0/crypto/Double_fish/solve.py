import string
from itertools import product
k = '_0m\K2!2%\ggrdups\\vd~gq'

def xor(str1, str2):
    """perform string xor on str1 and str2 and return string"""
    len_1 = len(str1)
    len_2 = len(str2)
    if len_1 >=len_2:
        return "".join(chr(ord(str1[i])^ord(str2[i%len_2])) for i in range(len_1) )
    else:
        return "".join(chr(ord(str1[i%len_1])^ord(str2[i])) for i in range(len_2) )


for keysize in range(1,3):
    possible_keys = []
    for key_pos in range(keysize):
        current_keys = []
        for ch in range(256):
            if all( i in string.printable[:95] for i in xor(chr(ch), k[key_pos::keysize] )):
                current_keys.append(chr(ch))
        possible_keys.append(current_keys)
    for key in product(*possible_keys):
        print(xor(k,"".join(key)))
