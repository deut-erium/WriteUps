from itertools import product
ct = "z_jjaoo_rljlhr_gauf_twv_shaqzb_ljtyut"
pseudo_key = "iigesssaemk"

pseudo_key_to_num = [ord(i)-97 for i in pseudo_key]
possible_keys = [ (i//2, i//2+13) for i in pseudo_key_to_num ]

ct_to_num = [ord(i)-97 if ord(i) >= 97 else i for i in ct ]
# _ preserved
# 2*i=10+26x
# i = 5+13x

def decrypt(ct,key):
    keylen = len(key)
    return "".join( ct[i] if str(ct[i])=='_' else chr((ct[i] - key[i%keylen] +26)%26 +97 ) for i in range(len(ct)) )


for key in product(*possible_keys):
    decrypted = decrypt(ct_to_num, key)
    print(decrypted,"".join(chr(i+97) for i in key ))
