from Crypto.PublicKey import RSA

with open("privkey_1.pem","r") as f:
    key = f.read()

rsakey = RSA.importKey(key)


