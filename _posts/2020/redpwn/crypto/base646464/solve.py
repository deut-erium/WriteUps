from base64 import b64decode

with open('cipher.txt','r') as cipher_file:
    data = cipher_file.read()

for i in range(25):
    data = b64decode(data)

print(data)
