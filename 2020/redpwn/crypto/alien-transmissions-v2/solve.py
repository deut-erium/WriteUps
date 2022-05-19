import z3
from z3 import *
import string
with open('encrypted.txt','r') as encrypted:
    data = list(map(int, encrypted.readlines()))

key = bytearray()
#for i in range(21*19):
#    data_slice = data[i::21*19]
#    key_char_val = 481 ^ max(data_slice, key=data_slice.count)
#    key.append(key_char_val)
#
#print(key)
key = bytearray(b'7G\x1a\x00x\x00l\x17X];9\x00Gj\x007Y\x013\x12\x00\x00-\x06\x14Vo\x1a\x0clnSn\x06]Ej7@\x04U7\x06AP\x17[;+Y\x06\x00\x12YC\x00++\x00\x073S[PB]CjnA7G7W\x04-A\x1cl7\x01_\x05X]\x16l\x16\x00\x00\x00\x00\x02j9E\x1a\x06+j[W\\\x08\x0clC\x06xA7E]l+\x0e\x02-\x00G<XZ\x089Y\x06-GO\x04j+\x1c[l9\x04AVD1\x0ck]S7G\x1a\x02\x12j+\x1c[ljURB[\x10\x00Y\x013\x12\x00\x02GlS]l+]\x00<V_\x16jEj7@\x04W]l\x06[\x14jjG\x0b\x031\x02nC\x00++\x00\x05Y9\x1c[Al\x12\x06<D\x06W\x00W\x04-A\x1cn]k\x18\x0e[lG\x00D\x051\x107\x02j9E\x1a\x04A\x00\x1c\\_9]\x00\x11\x03IQ\x00E]l+\x0e\x00Gj\x007[kYU\x0b\x03\x1cWx\x04j+\x1c[nSn\x06]G\x00]\x07\x0fV\x06W-\x02\x12j+\x1cY\x06\x00\x12YAjAl\x0b\x04\x02\x027\x02GlS]nA7G7UnG\x06\x17o\x06P3W]l\x06[\x16\x00\x00\x00\x00\x00\x00S\x02\x11\x05\x1a;7\x05Y9\x1c[C\x06xA7G7\x06l\x05\x01\x1cQ+n]k\x18\x0eY\x06-GO\x06\x00A[Po\x08U-\x04A\x00\x1c\\]S')


def get_models(F, M):
    result = []
    s = Solver()
    s.add(F)
    while len(result) < M and s.check() == sat:
        m = s.model()
        result.append(m)
        # Create a new constraint the blocks the current model
        block = []
        for d in m:
            # d is a declaration
            if d.arity() > 0:
                raise Z3Exception("uninterpreted functions are not supported")
            # create a constant from declaration
            c = d()
            if is_array(c) or c.sort().kind() == Z3_UNINTERPRETED_SORT:
                raise Z3Exception("arrays and uninterpreted sorts are not supported")
            block.append(c != m[d])
        s.add(Or(block))
    return result





key1 = [z3.BitVec("k1{}".format(i),8) for i in range(21)]
key2 = [z3.BitVec("k2{}".format(i),8) for i in range(19)]
F = []
for i in range(19*21):
    F.append(key1[i%21]^key2[i%19]==key[i])

# s.check()

VALID_CHARS = string.printable[0:62]+"_,.'?!@$<>*:-]*\\"
for model in get_models(F,256):
    KEY1 = "".join( chr(model[key1[i]].as_long()) for i in range(21))
    KEY2 = "".join( chr(model[key2[i]].as_long()) for i in range(19))
    flag = KEY1+KEY2
    if all(i in VALID_CHARS for i in flag):
        print(flag)

#h3r3'5_th3_f1r5t_h4lf_th3_53c0nd_15_th15
