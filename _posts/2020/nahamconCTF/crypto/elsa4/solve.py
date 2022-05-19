from pwn import remote
import re
import datetime
import random
import lc4
HOST, PORT = "jh2i.com", 50014

REM = remote(HOST, PORT)
initial_data = REM.recvuntil(b'>')
print(initial_data.decode())


def get_timestamp():
    hms = re.search(rb'(\d{2}):(\d{2}):(\d{2})', initial_data)
    ymd = re.search(rb'(\d{4})\/(\d{2})\/(\d{2})', initial_data)
    h, m, s = hms[1], hms[2], hms[3]
    y, mn, d = ymd[1], ymd[2], ymd[3]
    return map(int, tuple((y, mn, d, h, m, s)))


timestamp = datetime.datetime(*get_timestamp()).timestamp()
random.seed(int(timestamp))

nonce_length = 100  # some big number
alphabet = "#_23456789abcdefghijklmnopqrstuvwxyz"
nonce_chars = []
for _ in range(nonce_length):
    nonce_chars.extend(random.sample(alphabet, 1))


def encrypt(plaintext):
    REM.sendline(b'1')
    REM.sendline(plaintext)
    data = REM.recvuntil(b'>')
    key = re.search(
        b'Key = ([#_23456789abcdefghijklmnopqrstuvwxyz]+)',
        data)[1]
    encrypted = re.search(
        b'Encrypted = ([#_23456789abcdefghijklmnopqrstuvwxyz]+)',
        data)[1]
    return key, encrypted


def decryption_challenge():
    REM.sendline(b'2')
    data = REM.recvuntil(b'Decrypted =')
    key = re.search(
        b'Key = ([#_23456789abcdefghijklmnopqrstuvwxyz]+)',
        data)[1]
    encrypted = re.search(
        b'Encrypted = ([#_23456789abcdefghijklmnopqrstuvwxyz]+)',
        data)[1]
    return key, encrypted


def send_decryption(dec):
    REM.sendline(dec)
    data = REM.recvuntil(b'>')
    print(data.decode())

# def intify(message):
#     return [alphabet.index(i) for i in message]
#
# def diff_enc(m):
#     key, enc = encrypt(m)
#     print(key,enc)
#     key,enc = intify(key), intify(enc)
#     print(key)
#     print(enc)
#     return [a-b for a,b in zip(key,enc)]
