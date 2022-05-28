from pwn import remote
from hashlib import sha256
HOST, PORT = "localhost", 1337
HOST, PORT = "157.245.33.77", 30034

REM = remote(HOST, PORT)

REM.recvuntil(b'> ')

def get_output(cmd: bytes):
    REM.sendline(cmd)
    data = REM.recvuntil(b'> ')
    return bytes.fromhex(data[:-3].decode()) # strip b'\n> '


BLOCK_SIZE = 32

def encrypt_block(block, secret):
    enc_block = b''
    for i in range(BLOCK_SIZE):
        val = (block[i]+secret[i]) % 256
        enc_block += bytes([val])
    return enc_block


def encrypt(msg, password):
    h = sha256(password).digest()
    if len(msg) % BLOCK_SIZE != 0:
        msg = pad(msg, BLOCK_SIZE)
    blocks = [msg[i:i+BLOCK_SIZE] for i in range(0, len(msg), BLOCK_SIZE)]
    ct = b''
    for block in blocks:
        enc_block = encrypt_block(block, h)
        h = sha256(enc_block + block).digest()
        ct += enc_block
    return ct.hex()


def decrypt_block(block, secret):
    return encrypt_block(block, [(-i)%256 for i in secret])



def get_secret(block, known_plaintext):
    return decrypt_block(block, known_plaintext)

known_plaintext = b'Command executed: ' + b'cat secret.txt' + b'\n'
assert len(known_plaintext) >= 32

enc_flag = get_output(b'cat secret.txt')
secret = get_secret(enc_flag[:32], known_plaintext[:32])

def decrypt(enc_flag, h):
    pt = b''
    blocks = [enc_flag[i:i+BLOCK_SIZE] for i in range(0,len(enc_flag), BLOCK_SIZE)]
    for enc_block in blocks:
        block = decrypt_block(enc_block, h)
        h = sha256(enc_block + block).digest()
        pt += block
    return pt

dec_flag = decrypt(enc_flag, secret)
print(dec_flag)


# b'Command executed: cat secret.txt\nIn case Jenny malfunctions say the following phrase: Melt My Eyez, See Your Future  \nThe AI system will shutdown and you will gain complete control of the spaceship.\n- Danbeer S.A.\nHTB{b451c_b10ck_c1ph3r_15_w34k!!!}\n\x07\x07\x07\x07\x07\x07\x07'
