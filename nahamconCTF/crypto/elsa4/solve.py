from pwn import remote
import re
HOST, PORT = "jh2i.com", 50014

REM = remote(HOST,PORT)
print(REM.recvuntil(b'>').decode())


alphabet = b"#_23456789abcdefghijklmnopqrstuvwxyz"

def encrypt(plaintext):
    REM.sendline(b'1')
    REM.sendline(plaintext)
    data = REM.recvuntil(b'>')
    key = re.search(b'Key = ([#_23456789abcdefghijklmnopqrstuvwxyz]+)',data)[1]
    encrypted = re.search(b'Encrypted = ([#_23456789abcdefghijklmnopqrstuvwxyz]+)',data)[1]
    return key, encrypted

def decryption_challenge():
    REM.sendline(b'2')
    data = REM.recvuntil(b'Decrypted =')
    key = re.search(b'Key = ([#_23456789abcdefghijklmnopqrstuvwxyz]+)',data)[1]
    encrypted = re.search(b'Encrypted = ([#_23456789abcdefghijklmnopqrstuvwxyz]+)',data)[1]
    return key, encrypted

def send_decryption(dec):
    REM.sendline(dec)
    data = REM.recvuntil(b'>')
    print(data.decode())

def intify(message):
    return [alphabet.index(i) for i in message]

def diff_enc(m):
    key, enc = encrypt(m)
    print(key,enc)
    key,enc = intify(key), intify(enc)
    print(key)
    print(enc)
    return [a-b for a,b in zip(key,enc)]
