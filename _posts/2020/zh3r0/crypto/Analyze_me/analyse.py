
from Crypto.Util.number import *
from Crypto.Util.strxor import strxor
from binascii import *
from base64 import *
import random
from flags import *
import string


assert len(msg)==80

list1=list(msg[:len(msg)//2])
list2=list(msg[len(msg)//2:])

def from_the_bases(msg):
    i=random.randint(1,4)
    if i == 1:
        return b64encode(msg).decode().replace('=','')
    elif i == 2:
        return b32encode(msg).decode().replace('=','')
    elif i == 3 :
        return b85encode(msg).decode().replace('=','')
    else:
        return b16encode(msg).decode()

def rand_xor(lst):
    chr=random.choice(string.ascii_lowercase).encode()
    return [strxor(i.encode(),chr) for i in lst]


list3=rand_xor(list2)

list4=rand_xor(list1)

print('''Hello!
Welcome to Xor analysis..
There are two parts.
All the best ;)

Here is the first part:

''')
for i in list3:
    print(bytes_to_long(from_the_bases(i).encode()),end='|')
for j in list4:
    print(bytes_to_long(from_the_bases(i).encode()),end='|')

print()

user_input=input('Enter the decoded message:')

assert len(user_input)==80

if user_input==msg:
    print('You have done well.')
    print('Here is the key: ',bytes_to_long(key.encode()))

else:
    print('Try harder ;)')
    quit()

print('\nYou completed the first part \n Here is the second and final part ;) ')

print('GOOD LUCK DECODING!!! \n')


table={'0':{'0':'63','1':'7c','2':'77','3':'7b','4':'f2','5':'6b','6':'6f','7':'c5','8':'30','9':'01','a':'67','b':'2b','c':'fe','d':'d7','e':'ab','f':'76'},
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

flag=final_flag#final_flag is a variable from my flags module

final_key=key#key is a variable from my flags module, ohhh you have the key if you solved the first part

list_flag=[hexlify(flag[i:i+4].encode()).decode() for i in range(0,len(flag),4) ]

final_list=[]

rand_num=random.randint(2,4)

for c in list_flag:
    chr=c
    num=0
    while num < rand_num:
        chr=table[chr[0]][chr[1]]+table[chr[2]][chr[3]]+table[chr[4]][chr[5]]+table[chr[6]][chr[7]]
        num+=1
    final_list.append(chr)

key_list=[hexlify(final_key[i:i+4].encode()).decode() for i in range(0,len(key),4)]

xor_list=[strxor(i.encode(),j.encode()) for i,j in zip(final_list,key_list)]

print(xor_list)

user_input=input('Enter the flag:')

if user_input==final_flag:
    print('Perfect you got the flag ;) \nGo submit it!!!')

else:
    print('You must try harder!!!!!!!')
    quit()
