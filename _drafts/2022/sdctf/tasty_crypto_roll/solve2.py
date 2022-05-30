import random
from tqdm import tqdm
from Crypto.Cipher import AES

# set DEBUG to true to see the recursion progress for bruteforcing
DEBUG = 0

cip = open('enc.bin', 'rb').read()

def to_binary(b: bytes):
	assert isinstance(b, bytes)
	return ''.join(['{:08b}'.format(c) for c in b])

def from_binary(s: str):
	assert isinstance(s, str)
	return bytes(int(s[i:i+8], 2) for i in range(0, len(s), 8))

def encrypt(key: bytes, message: bytes):
	cipher = AES.new(key, AES.MODE_ECB)
	return cipher.encrypt(message) 

def decrypt(key: bytes, message: bytes):
	cipher = AES.new(key, AES.MODE_ECB)
	return cipher.decrypt(message) 

if False: # code to get key1, the idea is to bet on collision of 220 utf-8 characters.
	MAX_PID = 1 << 15
	for key1 in tqdm(range(MAX_PID)):
		random.seed(key1)
		key_final = bytes(random.randrange(256) for _ in range(16))
		c = decrypt(key_final, cip)

		c_bits = list(to_binary(c))
		p = [i for i in range(len(c_bits))]
		random.shuffle(p)
		_p = [i for i in range(len(p))]
		for i in range(len(p)):
			_p[p[i]] = i

		pt_bits = ''.join(c_bits[i] for i in _p)

		pt = from_binary(pt_bits)
		blocks = [pt[i:i+16] for i in range(0, len(pt), 16)]
		if len(blocks) != len(set(blocks)):
			print(key1)
			break

key1 = 83

if True: # reverse the part that use key_final
	random.seed(key1)
	key_final = bytes(random.randrange(256) for _ in range(16))
	c = decrypt(key_final, cip)

	c_bits = list(to_binary(c))
	p = [i for i in range(len(c_bits))]
	random.shuffle(p)
	_p = [i for i in range(len(p))]
	for i in range(len(p)):
		_p[p[i]] = i

	pt_bits = ''.join(c_bits[i] for i in _p)

	cip = from_binary(pt_bits)

# 4 AES blocks => 8 bytes/4 characters => single sbox => single flag bytes
# here we relabel all characters & AES blocks with number between 0 ~ 255
mp = dict()
counter = 0

for i in range(0, len(cip), 16):
	if cip[i:i+16] not in mp:
		mp[cip[i:i+16]] = counter
		counter += 1

# After relabelling, we first get information by checking within-character repetition

print("Ciphertext repetition:")
cip = [mp[cip[i:i+16]] for i in range(0, len(cip), 16)] 
cip = [cip[i:i+4] for i in range(0, len(cip), 4)]
for c in cip:
	if len(set(c)) != len(c):
		print(c)

codes = sum([[i, i] for i in range(256)], start=[]) # notice that the range is changed from [0xb0, 0x1b0) to [0, 256). It's just for relabeling.
random.seed(key1)
random.shuffle(codes)
sboxes = [codes[i*4:(i+1)*4] for i in range(128)]

print("Sbox repetition:")
for s in sboxes:
	if len(set(s)) != 4:
		print(s)

# Bruteforcing starts from here

def match(a, b):
	for x, y in zip(a, b):
		if x == -1 or y == -1:
			continue
		if x != y:
			return False

	return True

answers = []

def getFlag(cip, sboxes, mp): # get the flag based on current mapping, unknown char will be shown as '?'
	res = []
	for c in cip:
		afterMap = [mp.get(x, -1) for x in c]
		found = False
		for i, s in enumerate(sboxes):
			if s == afterMap:
				res.append(i)
				found = True
				break
		if not found:
			res.append(ord('?'))
	return bytes(res)

def brute(cip, sboxes, mp):
	"""
	cip and sboxes remain unchanged throughout the recursive call, but I feel bad using global varaibles.
	"""
	if DEBUG:
		print(getFlag(cip, sboxes, mp))

	# check is finished
	isFinished = True
	for c in cip:
		if all(x in mp for x in c):
			pass
		else:
			isFinished = False

	if isFinished:
		answers.append(getFlag(cip, sboxes, mp))
		print("Found an answer!!!!!!!")
		return

	# try matching
	isContradiction = False
	mp = mp.copy()

	# Find the one with least possible matches.
	min_pos = 256
	index = -1

	for idx, c in enumerate(cip):
		afterMap = [mp.get(x, -1) for x in c]
		if -1 not in afterMap:
			continue

		matches = [s for s in sboxes if match(s, afterMap)]

		if len(matches) == 0:
			isContradiction = True
			break

		if min_pos > len(matches):
			index = idx
			min_pos = len(matches)

	if isContradiction:
		return
	
	# now bruteforce all possibilities
	assert index != -1
	afterMap = [mp.get(x, -1) for x in cip[index]]
	matches = [s for s in sboxes if match(s, afterMap)]
	for m in matches:
		for x, y in zip(cip[index], m):
			mp[x] = y
		brute(cip, sboxes, mp)

# This is based on the repetition
for _ in [132, 197]:
	mp = {35: 224, 109: 144, 4: _}
	brute(cip, sboxes, mp)

print("Answers:")
answers = list(set(answers))
for x in answers:
	print(b"sdctf{" + x + b"}")

# The fourth one is the actual answer