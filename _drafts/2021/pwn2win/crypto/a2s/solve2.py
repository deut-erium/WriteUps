from a2s import *
from z3 import BitVec, BitVecSort, BitVecVal, Function, Solver, If, simplify,set_option
set_option(unsat_core=True)

plaintexts =  ['0573e60e862b4c46bdc5fcea1d0316ea', '2dd6d234bfe14fb0a0c4786b3891698d', '533698ece7db47df82413aba5f4f0cfb']
ciphertexts =  ['42352473eeb42625210217a339dbc69f', 'b14c9d2d835c725e13598907a5b89165', 'f96b99b82fe4543150604d20e8cd5fda']
ciphertexts = [bytes.fromhex(i) for i in ciphertexts]
plaintexts = [bytes.fromhex(i) for i in plaintexts]
iv =  bytes.fromhex('35a84c9bf33d40e8bfab6e7e62209b49')
encrypted_flag =  bytes.fromhex('ef14d5f8f4f51b34fb251bacf309e0c4386c33021903528b475d232a401aeeb49e23b3bc2a416b386590ae0d5580cbfebce4a40ed563f664f28d1cfa8e4cde02bfe077b1ef583bf2850cf0ac764182e7')
key = bytearray([0x3])+bytearray(14)+bytearray([0x39])


KEY = [BitVec(f'KEY[{i}]',8) for i in range(16)]
SBOX = Function('SBOX',BitVecSort(8),BitVecSort(8))
INV_SBOX = Function('SBOX',BitVecSort(8), BitVecSort(8))
KEY[0] = BitVecVal(0x3,8)
KEY[-1] = BitVecVal(0x39,8)
# EXPAND ROUND KEYS
key_columns = bytes2matrix(KEY)
i = 1
while len(key_columns) < 3*4:
    word = list(key_columns[-1])
    if len(key_columns)%4==0:
        word.append(word.pop(0))
        word = [SBOX(b) for b in word]
        word[0]^=r_con[i]
        i+=1
    word = [ i^j for i,j in zip(word,key_columns[-4])]
    key_columns.append(word)
round_keys = [key_columns[4*i:4*(i+1)] for i in range(len(key_columns)//4)]

xtime_z3 = lambda a: If( a&0x80==0x80, (a<<1)^0x1b, a<<1)

def sub_bytes_z3(s):
    for i in range(4):
        for j in range(4):
            s[i][j] = SBOX(s[i][j])

def inv_sub_bytes_z3(s):
    for i in range(4):
        for j in range(4):
            s[i][j] = INV_SBOX(s[i][j])

def mix_single_column_z3(a):
    t = a[0]^a[1]^a[2]^a[3]
    u = a[0]
    a[0] ^= t^xtime_z3(a[0]^a[1])
    a[1] ^= t^xtime_z3(a[1]^a[2])
    a[2] ^= t^xtime_z3(a[2]^a[3])
    a[3] ^= t^xtime_z3(a[3]^u)

def mix_columns_z3(s):
    for i in range(4):
        mix_single_column_z3(s[i])

def inv_mix_columns_z3(s):
    for i in range(4):
        u = xtime_z3(xtime_z3(s[i][0] ^ s[i][2]))
        v = xtime_z3(xtime_z3(s[i][1] ^ s[i][3]))
        s[i][0] ^= u
        s[i][1] ^= v
        s[i][2] ^= u
        s[i][3] ^= v
    mix_columns_z3(s)

def simplify_plain_state(plain_state):
    for i in range(4):
        for j in range(4):
            plain_state[i][j] = simplify(plain_state[i][j])

def encrypt(pt):
    plain_state = bytes2matrix(pt)

    add_round_key(plain_state,round_keys[0])
    sub_bytes_z3(plain_state)
    shift_rows(plain_state)
    mix_columns_z3(plain_state)
    simplify_plain_state(plain_state)

    add_round_key(plain_state,round_keys[1])
    sub_bytes_z3(plain_state)
    shift_rows(plain_state)
    mix_columns_z3(plain_state)
    simplify_plain_state(plain_state)

    add_round_key(plain_state,round_keys[2])
    simplify_plain_state(plain_state)
    res_bytes = []
    for i in plain_state:
        res_bytes.extend(i)
    return res_bytes

def encrypt_constraints(pt,ct):
    plain_state = bytes2matrix(pt)

    add_round_key(plain_state,round_keys[0])
    sub_bytes_z3(plain_state)
    shift_rows(plain_state)
    mix_columns_z3(plain_state)

    #add_round_key(plain_state,round_keys[1])

    ct_state = bytes2matrix(ct)
    add_round_key(ct_state,round_keys[2])
    inv_mix_columns_z3(ct_state)
    inv_shift_rows(ct_state)
    inv_sub_bytes_z3(ct_state)

    constraints = []
    for i in range(4):
        for j in range(4):
            constraints.append(ct_state[i][j]^plain_state[i][j]==round_keys[1][i][j])
    return constraints


solver = Solver()
for i in range(256):
    solver.add(SBOX(i)==s_box[i])
    solver.add(INV_SBOX(i)==inv_s_box[i])
#
for pt,ct in zip(plaintexts,ciphertexts):
    solver.add(encrypt_constraints(pt,ct))

