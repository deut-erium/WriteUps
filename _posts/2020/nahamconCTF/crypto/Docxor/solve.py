from pwn import xor

with open('homework','rb') as homework_file:
    homework_data = homework_file.read()

header = homework_data[0:4]
magic = b"\x50\x4B\x03\x04"
key = xor(header,magic)

with open('decrypted.doc','wb') as decrypted:
    decrypted.write(xor(key,homework_data))
