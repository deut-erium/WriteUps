from Crypto.Cipher import DES
with open('ciphertext', 'rb') as ct_file:
    ct = ct_file.read()

weak_keys = [
    b'\x01\x01\x01\x01\x01\x01\x01\x01',
    b'\xFE\xFE\xFE\xFE\xFE\xFE\xFE\xFE',
    b'\xE0\xE0\xE0\xE0\xF1\xF1\xF1\xF1',
    b'\x1F\x1F\x1F\x1F\x0E\x0E\x0E\x0E'
]

for key in weak_keys:
    iv = b"13371337"
    des = DES.new(key, DES.MODE_OFB, iv)
    pt = des.decrypt(ct)
    print(pt)
