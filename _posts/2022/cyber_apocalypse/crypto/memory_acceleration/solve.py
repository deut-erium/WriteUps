from z3 import *
from hashlib import md5
from Crypto.Util.number import long_to_bytes, bytes_to_long
from pofwork import rotl, sub, phash, sbox
from tqdm import tqdm


def hack_proof_of_work(message):
	block = md5(message).digest()
	block = 4*block
	blocks = [int.from_bytes(block[i:i+4],'big') for i in range(0, len(block), 4)]
	rv1, rv2 = BitVecVal(0x2423380b4d045,32), BitVecVal(0x3b30fa7ccaa83,32)
	key1 = BitVec('key1', 32)
	key2 = BitVec('key2', 32)
	m = 0xffffffff
	x, y, z, u = key1, *[BitVecVal(i,32) for i in (0x39ef52e9f30b3, 0x253ea615d0215, 0x2cd1372d21d77)]
	for i in range(13):
		x,y = blocks[i] ^ x, blocks[i+1] ^ y
		z,u = blocks[i+2] ^ z, blocks[i+3] ^ u
		x,y,z,u = [simplify(i) for i in (x,y,z,u)]
		x = x*(m + LShR(y,16)) ^ RotateLeft(z, 3)
		rv1 ^= x
		y = y*(m + LShR(z,16)) ^ RotateLeft(x, 3)
		rv2 ^= y
		rv1, rv2 = rv2, rv1
		rv1 = sub(rv1)

	SBOX = Array('SBOX', BitVecSort(8), BitVecSort(8))
	def sub(bitvec32):
		vec_bytes = [Extract(8*i+7, 8*i, bitvec32) for i in range(3,-1,-1)]
		return Concat([SBOX[i] for i in vec_bytes])

	h = simplify(rv1 + 0x6276137d7)
	subkey2 = [Extract(8*i+7,8*i,key2) for i in range(3,-1,-1)]
	subkey2 = [SBOX[i] for i in subkey2]
	subkey2 = [ZeroExt(24,i) for i in subkey2]

	for i,d in enumerate(subkey2):
		a = (h<<1)
		b = (h<<3)
		c = LShR(h,4)
		h ^= (a+b+c-d)
		h += h
	h ^= u*z
	solver = Solver()
	solver.add(h==0)
	for i,v in enumerate(sbox):
		solver.add(SBOX[i]==v)
	if solver.check() == sat:
		m = solver.model()
		return (m[key1].as_long(), m[key2].as_long())

def hack_only_key2(h,nbits=0):
    # note its post substitution for less complexity and speed
    # nbits is the number of nonzero most significant bits we can tolerate
    h = BitVecVal(h,32)
    key2 = BitVec('key2',32)
    subkey2 = [Extract(8*i+7,8*i,key2) for i in range(3,-1,-1)]
    subkey2 = [ZeroExt(24,i) for i in subkey2]
    for i,d in enumerate(subkey2):
        a = (h<<1)
        b = (h<<3)
        c = LShR(h,4)
        h ^= (a+b+c-d)
        h += h
    solver = Solver()
    solver.add(Extract(31-nbits,0,h)==0)
    if solver.check() == sat:
        m = solver.model()
        return m[key2].as_long()

def zerocount(num):
    count = 0
    while num&1==0:
        count+=1
        num>>=1
    return count

def phashk1(block, key1):
    block = md5(block.encode()).digest()
    block = 4 * block
    blocks = [bytes_to_long(block[i:i+4]) for i in range(0, len(block), 4)]

    m = 0xffffffff
    rv1, rv2 = 0x2423380b4d045, 0x3b30fa7ccaa83
    x, y, z, u = key1, 0x39ef52e9f30b3, 0x253ea615d0215, 0x2cd1372d21d77

    for i in range(13):
        x, y = blocks[i] ^ x, blocks[i+1] ^ y
        z, u = blocks[i+2] ^ z, blocks[i+3] ^ u
        rv1 ^= (x := (x & m) * (m + (y >> 16)) ^ rotl(z, 3))
        rv2 ^= (y := (y & m) * (m + (z >> 16)) ^ rotl(x, 3))
        rv1, rv2 = rv2, rv1
        rv1 = sub(rv1)
        rv1 = bytes_to_long(rv1)
    h = rv1 + 0x6276137d7 & m
    return h,zerocount(u*z)

def form_blocks(block):
    """making bruteforce faster by removing recomputation of md5"""
    block = md5(block.encode()).digest()
    block = 4 * block
    blocks = [bytes_to_long(block[i:i+4]) for i in range(0, len(block), 4)]
    return blocks

def phashk1(blocks, key1):
    """hash state till key1 part and before key2 substitution"""
    m = 0xffffffff
    rv1, rv2 = 0x2423380b4d045, 0x3b30fa7ccaa83
    x, y, z, u = key1, 0x39ef52e9f30b3, 0x253ea615d0215, 0x2cd1372d21d77

    for i in range(13):
        x, y = blocks[i] ^ x, blocks[i+1] ^ y
        z, u = blocks[i+2] ^ z, blocks[i+3] ^ u
        rv1 ^= (x := (x & m) * (m + (y >> 16)) ^ rotl(z, 3))
        rv2 ^= (y := (y & m) * (m + (z >> 16)) ^ rotl(x, 3))
        rv1, rv2 = rv2, rv1
        rv1 = sub(rv1)
        rv1 = bytes_to_long(rv1)
    h = rv1 + 0x6276137d7 & m
    # also return the number of zeros in u*z so our model finds it easier
    return h,zerocount(u*z)

def desubstitute(key2):
    desub_bytes =  bytes([sbox.index(i) for i in int.to_bytes(key2,4,'big')])
    return int.from_bytes(desub_bytes,'big')

def bruteforce_key1(block):
    blocks = form_blocks(block)
    for key1 in tqdm(range(2**32),total=-1):
        h, nbits = phashk1(blocks, key1)
        key2 = hack_only_key2(h, nbits)
        if key2:
            return key1, desubstitute(key2)


