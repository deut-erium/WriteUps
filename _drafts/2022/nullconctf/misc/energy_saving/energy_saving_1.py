#!/usr/bin/env python3

import sys
from Crypto.PublicKey import RSA
from Crypto.Util.number import bytes_to_long, long_to_bytes

from secret import cipher

LIMIT = 2450
key = RSA.import_key(open('privkey.pem','r').read())


text = '''Facing both the energy crisis cause by Russia's war and Global Warming, we have to save energy wherever we can.
So, for my RSA decryption I only have a single register, can load one other value from memory and I am allowed only %d modular multiplications, but the standard method needs over 3000.
Can you help me decrypt the message I got? If it's nothing private, I will share it with you. I even give you my private key.
''' % LIMIT

def loop():
	while True:
		print('Load cipher into register.')
		register = cipher
		current_power = 1
		results = {1:cipher}
		for _ in range(LIMIT):
			print('Currently loaded exponent: %d' % current_power)
			print('Which power of the cipher should I multiply to my register? Tell me the exponent:')
			sys.stdout.flush()
			number = int(sys.stdin.buffer.readline().strip().decode())
			if number == 0: break
			if number not in results:
				print('I haven\'t computed that result, yet.')
				break
			register *= results[number]
			register %= key.n
			current_power += number
			results[current_power] = register
		msg = long_to_bytes(register)
		if msg[:4] == b'ENO{':
			print(msg.decode())
		else:
			print('This may be sensitive information. Let\'s start again.\n')

if __name__ == '__main__':
	print(text)
	try:
		loop()
	except Exception as err:
		print(repr(err))
