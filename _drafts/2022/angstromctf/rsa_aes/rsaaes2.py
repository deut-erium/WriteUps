from Crypto.Util.number import bytes_to_long, long_to_bytes, getPrime
from Crypto.Util.Padding import pad
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES

p = getPrime(1024)
q = getPrime(1024)
n = p*q
# print(n)
print(p)
print(q)
e = 0x10001
d = pow(e,-1, (p-1)*(q-1))
flag = 962424730933711583982509475866271719924314715515263277362282856891434254676830516728587380223284413277330392754127799728228693422747053
# flag_facs = [3, 41, 71, 607, 6299, 6673, 11311, 11489, 14951, 16091, 17977, 19079, 20233, 23011, 27919, 28277, 29537, 29599, 35963, 36847, 37589, 40903, 48781, 50129, 50839, 55331, 62459, 63029, 63317, 66683, 67121, 71471, 76159, 80491, 80681, 80803, 81353, 85201, 85853, 87623]
# flag_facs = [2081, 271, 811, 1709, 3697, 1187, 2333, 9857, 6703, 3301, 8647, 5417, 5449, 6359, 4001, 7993, 3691, 2281, 3449, 8539, 8209, 9419, 1069, 5659, 5179, 1291, 1013, 1093, 251, 9157, 593, 7717, 8597, 1259, 223, 3001, 491, 71, 4951, 941]

assert pow(2,e*d,n)==2

enc = pow(flag,e,n)
print(enc)

k = get_random_bytes(32)
iv = get_random_bytes(16)
cipher = AES.new(k, AES.MODE_CBC, iv)

while 1:
	try:
		i = int(input("Enter message to sign: "))
		assert(0 < i < n)
		print("signed message (encrypted with military-grade aes-256-cbc encryption):")
		print(cipher.encrypt(pad(long_to_bytes(pow(i,d,n)),16)))
	except:
		print("bad input, exiting")
