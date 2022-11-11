
#!/usr/bin/env python3

from struct import pack, unpack
flag = b'darkCON{XXXXXXXXXXXXXXXXXXX}'

def Tup_Int(chunk):
	return unpack("I",chunk)[0]

chunks = [flag[i*4:(i+1)*4] for i in range(len(flag)//4)]
ciphertext = ""

f = open('cipher.txt','w')
for i in range(len(chunks) - 2):
	block = pack("I", Tup_Int(chunks[i]) ^ Tup_Int(chunks[i+2]))
	ciphertext = 'B' + str(i) + ' : ' + str(block) + '\n'
	f.write(ciphertext)


B = [b'\nQ&4',b"\x17'\x0e\x0f",b'1X5\r',b'072E',b'\x18\x00\x15/']
flag = b'darkCON{n0T_Th@t_haRd_r1Ght}'
