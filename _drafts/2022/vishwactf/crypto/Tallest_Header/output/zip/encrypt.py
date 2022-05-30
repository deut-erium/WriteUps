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
