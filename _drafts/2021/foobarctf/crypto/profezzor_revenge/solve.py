from pwn import xor
with open('assignment','rb') as f:
    enc_file = f.read()

pdf_header = b'%PDF-1.3'
key = xor(pdf_header,enc_file[:len(pdf_header)])

decrypted = xor(key,enc_file)

with open('decrypted.pdf','wb') as f:
    f.write(decrypted)
