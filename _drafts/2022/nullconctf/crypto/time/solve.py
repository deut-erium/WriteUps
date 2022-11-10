from Crypto.PublicKey import RSA

with open("pubkey.pem","r") as f:
    key = f.read()

rsakey = RSA.importKey(key)


