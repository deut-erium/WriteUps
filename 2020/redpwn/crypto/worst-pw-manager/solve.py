import itertools
import string
import os
from pwn import xor

def decode_filename(file_name):
    num, mask = file_name.split('_')
    file_mask = mask.split('.enc')[0]
    password = ""
    for i in range(len(file_mask)):
        char = file_mask[i]
        if char.isdigit():
            password+=chr( (ord(char)-ord("0")-i+10)%10 + ord('0')  )
        else:
            password+=chr( (ord(char)-ord("a")-i+26)%26 + ord('a')  )
    return password,int(num)

def get_passwords():
    p_ct_list = []
    for file_name in os.listdir('worst-pw-manager/passwords'):
        password, num = decode_filename(file_name)
        with open('worst-pw-manager/passwords/'+file_name,'rb') as enc_file:
            encrypted = enc_file.read()
        p_ct_list.append([num,password,encrypted])
    return p_ct_list

class KeyByteHolder(): # im paid by LoC, excuse the enterprise level code
    def __init__(self, num):
        assert num >= 0 and num < 256
        self.num = num

    def __repr__(self):
        return hex(self.num)[2:]

def rc4(text, key): # definitely not stolen from stackoverflow
    S = [i for i in range(256)]
    j = 0
    out = bytearray()

    #KSA Phase
    for i in range(256):
        j = (j + S[i] + key[i % len(key)]) % 256
        S[i] , S[j] = S[j] , S[i]

    #PRGA Phase
    i = j = 0
    for char in text:
        i = ( i + 1 ) % 256
        j = ( j + S[i] ) % 256
        S[i] , S[j] = S[j] , S[i]
        out.append(ord(char) ^ S[(S[i] + S[j]) % 256])

    return out

VALID_CHAR =  '(){}'+string.printable[0:62]+"_,.'?!@$<>*:-]*\\"
VALID_ORD = [ord(i) for i in VALID_CHAR]
def bruteforce(pt,ct,key_crib):
    bf_len = 8-len(key_crib)
    for addend in itertools.combinations_with_replacement(VALID_ORD,bf_len):
#key1 = bytearray(key_crib)+bytearray(addend)
#       for circular in range(bf_len):
#key = key1[-circular:]+key1[:-circular]
        key=bytearray(key_crib)+bytearray(addend)
        if rc4(pt,key) == ct:
            print(key)
            return key

def bruteforce_keylast(pt,ct):
    for i in range(256):
        key = bytearray([i for _ in range(8)])
        if rc4(pt,key) == ct:
            return i

data = get_passwords()
data = sorted(data, key = lambda x:x[0])
eighth_chars = [(ind,bruteforce_keylast(pt,ct)) for ind,pt,ct in data ]

for flag_len in range(9,50):
    flag = bytearray(flag_len)
    for ind,key_char in eighth_chars:
        starting_ind = (ind*8)%flag_len
        flag[(starting_ind+8)%flag_len] = key_char
    if b'flag' in flag:
        print(flag.decode())
        break

#flag{crypto_is_stupid_and_python_is_stupid}

