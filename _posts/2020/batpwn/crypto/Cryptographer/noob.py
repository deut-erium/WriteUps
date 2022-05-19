#!/usr/bin/env python2
# I AM NOOB :)
import string
from hashlib import md5
from itertools import izip, cycle
import base64
import time

def xor(data, key): 
    return bytearray(a^b for a, b in zip(*map(bytearray, [data, key]))) 

flag=""
   
timestamp = time.time()
print int(timestamp)
key = md5(str(int(timestamp))).hexdigest()
my_hexdata = key

scale = 16 
num_of_bits = 8
noobda = bin(int(my_hexdata, scale))[2:].zfill(num_of_bits)
print noobda
xorer(flag,noobda)
noobie = base64.encodestring(xorer).strip()
print noobie



