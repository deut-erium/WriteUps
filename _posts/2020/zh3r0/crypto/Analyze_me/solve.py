from pwn import remote, xor
from base64 import b32decode, b64decode, b85decode, b16decode
from Crypto.Util.number import long_to_bytes
import binascii
import string

HOST, PORT = "crypto.zh3r0.ml", 3871

REM = remote(HOST, PORT)

chal1 = REM.recvuntil(b'Enter the decoded message:')
print(chal1.decode())

chal1_data = chal1.split(b'\n\n\n')[1].split(b'|\n')[0].split(b'|')
chal1_data = [long_to_bytes(int(i)) for i in chal1_data]

#VIABLE_SET = set( xor(i, j) for i in string.ascii_lowercase.encode() for j in string.printable[:95].encode() )
PRINTABLE = string.printable.encode()

def check_valid(string):
    return all(i in PRINTABLE for i in string)


def decode(m):
    res = []
    try:
        val = bytes.fromhex(m.decode())
        if not check_valid(val):
            raise ValueError
        res.append(val)
    except ValueError:
        try:
            val = b32decode(m)
            if not check_valid(val):
                raise ValueError
            res.append(val)
        except (binascii.Error, ValueError):
            try:
                val = b64decode(m)
                if not check_valid(val):
                    raise ValueError
                res.append(val)
            except (binascii.Error, ValueError):
                try:
                    val = b85decode(m)
                    res.append(val)
                except binascii.Error:
                    pass
    return res

part_1 = b''.join( decode(i)[0] for i in chal1_data )
print(part_1.decode())
REM.sendline(part_1)

data = REM.recvuntil(b'Enter the flag:')
print(data.decode())
data = data.split(b'\n')

KEY = long_to_bytes(int(data[1].split()[-1]))
flag_enc = eval(data[7])

TABLE={'0':{'0':'63','1':'7c','2':'77','3':'7b','4':'f2','5':'6b','6':'6f','7':'c5','8':'30','9':'01','a':'67','b':'2b','c':'fe','d':'d7','e':'ab','f':'76'},
       '1':{'0':'ca','1':'82','2':'c9','3':'7d','4':'fa','5':'59','6':'47','7':'f0','8':'ad','9':'d4','a':'a2','b':'af','c':'9c','d':'a4','e':'72','f':'c0'},
       '2':{'0':'b7','1':'fd','2':'93','3':'26','4':'36','5':'3f','6':'f7','7':'cc','8':'34','9':'a5','a':'e5','b':'f1','c':'71','d':'d8','e':'31','f':'15'},
       '3':{'0':'04','1':'c7','2':'23','3':'c3','4':'18','5':'96','6':'05','7':'9a','8':'07','9':'12','a':'80','b':'e2','c':'eb','d':'27','e':'b2','f':'75'},
       '4':{'0':'09','1':'83','2':'2c','3':'1a','4':'1b','5':'6e','6':'5a','7':'a0','8':'52','9':'3b','a':'d6','b':'b3','c':'29','d':'e3','e':'2f','f':'84'},
       '5':{'0':'53','1':'d1','2':'00','3':'ed','4':'20','5':'fc','6':'b1','7':'5b','8':'6a','9':'cb','a':'be','b':'39','c':'4a','d':'4c','e':'58','f':'cf'},
       '6':{'0':'d0','1':'ef','2':'aa','3':'fb','4':'43','5':'4d','6':'33','7':'85','8':'45','9':'f9','a':'02','b':'7f','c':'50','d':'3c','e':'9f','f':'a8'},
       '7':{'0':'51','1':'a3','2':'40','3':'8f','4':'92','5':'9d','6':'38','7':'f5','8':'bc','9':'b6','a':'da','b':'21','c':'10','d':'ff','e':'f3','f':'d2'},
       '8':{'0':'cd','1':'0c','2':'13','3':'ec','4':'5f','5':'97','6':'44','7':'17','8':'c4','9':'a7','a':'7e','b':'3d','c':'64','d':'5d','e':'19','f':'73'},
       '9':{'0':'60','1':'81','2':'4f','3':'dc','4':'22','5':'2a','6':'90','7':'88','8':'46','9':'ee','a':'b8','b':'14','c':'de','d':'5e','e':'0b','f':'db'},
       'a':{'0':'e0','1':'32','2':'3a','3':'0a','4':'49','5':'06','6':'24','7':'5c','8':'c2','9':'d3','a':'ac','b':'62','c':'91','d':'95','e':'e4','f':'79'},
       'b':{'0':'e7','1':'c8','2':'37','3':'6d','4':'8d','5':'d5','6':'4e','7':'a9','8':'6c','9':'56','a':'f4','b':'ea','c':'65','d':'7a','e':'ae','f':'08'},
       'c':{'0':'ba','1':'78','2':'25','3':'2e','4':'1c','5':'a6','6':'b4','7':'c6','8':'e8','9':'dd','a':'74','b':'1f','c':'4b','d':'bd','e':'8b','f':'8a'},
       'd':{'0':'70','1':'3e','2':'b5','3':'66','4':'48','5':'03','6':'f6','7':'0e','8':'61','9':'35','a':'57','b':'b9','c':'86','d':'c1','e':'1d','f':'9e'},
       'e':{'0':'e1','1':'f8','2':'98','3':'11','4':'69','5':'d9','6':'8e','7':'94','8':'9b','9':'1e','a':'87','b':'e9','c':'ce','d':'55','e':'28','f':'df'},
       'f':{'0':'8c','1':'a1','2':'89','3':'0d','4':'bf','5':'36','6':'42','7':'68','8':'41','9':'99','a':'2d','b':'0f','c':'b0','d':'54','e':'bb','f':'16'}}

INV_TABLE = {}
for k,v in TABLE.items():
    for key,val in v.items():
        INV_TABLE[val] = k+key

flag_unxored = bytes.fromhex(xor(b''.join(flag_enc),KEY.hex().encode()).decode())

for _ in range(4):
    flag = ""
    for i in flag_unxored:
        flag+=INV_TABLE[hex(i)[2:].zfill(2)]
    flag = bytes.fromhex(flag)
    if b'zh3r0' in flag:
        print(flag)
        break
    flag_unxored = flag


