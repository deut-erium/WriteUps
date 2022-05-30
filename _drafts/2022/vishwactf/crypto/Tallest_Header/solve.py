key = [2,1,3,5,4]
import string
ciphertext = "RT1KC _YH43 3DRW_ T1HP_ R3M7U TA1N0"

def encrypt(key, plaintext):
    plaintext = "".join(plaintext.split(" ")).upper()
    ciphertext = ""
    for pad in range(0, len(plaintext) % len(key) * -1 % len(key)):
        plaintext += "X"
    for offset in range(0, len(plaintext), len(key)):
        for element in [a - 1 for a in key]:
            ciphertext += plaintext[offset + element]
        ciphertext += " "
    return ciphertext[:-1]

def decrypt(key, ciphertext):
    order = [ord(i) - ord('A') for i in encrypt(key, string.ascii_uppercase[:25]).replace(' ','')]
    plaintext = [None]*25
    ciphertext = ciphertext.replace(' ','')
    for i,v in enumerate(order):
        plaintext[v] = ciphertext[i]
    return "".join(plaintext).lower()
print(decrypt(key, ciphertext))

