import pwn
import base64
from Crypto.Cipher import AES
from Crypto.Hash import SHA3_256, HMAC, BLAKE2s
from Crypto.Random import urandom, random
pwn.context(log_level=1000)

def int_to_bytes(i):
    return i.to_bytes((i.bit_length() + 7) // 8, byteorder='big')

def encode(s):
    bits = bin(int.from_bytes(s, byteorder='big'))[2:]
    ret = ''

    for bit in bits:
        if bit == '1':
            if random.randrange(0,2):
                ret += '01'
            else:
                ret += '10'
        else:
            ret += '00'

    return int_to_bytes(int(ret, base=2))

def decode(s):
    bits = bin(int.from_bytes(s, byteorder='big'))[2:]
    if len(bits) % 2:
        bits = '0' + bits

    ret = ''

    for i in range(0,len(bits)-1,2):
        if int(bits[i] + bits[i+1],base=2):
            ret += '1'
        else:
            ret += '0'

    return int_to_bytes(int(ret, base=2))

def decrypt(c):
    try:
        aes = AES.new(key=encryption_key, mode=AES.MODE_CTR,nonce=c[:8])

        decrypted = aes.decrypt(c[8:])
        message, tag = decode(decrypted[:-16]), decrypted[-16:]

        HMAC.new(key=mac_key, msg=message).verify(mac_tag=tag)
        return message
    except ValueError:
        print("Get off my lawn or I call the police!!!")
        exit(1)

enc_pass = b'kgsekWGeAwPhz6tbMyLd34Bg5pwhy2TkQJF7NRYC987Ibuiu/dmNHqyYXHV0kXlksThSRi83Qu2owAiUdT9pfqlY'
orig_pass = base64.b64decode(enc_pass)
nonce, orig_pass, tag = orig_pass[:8], orig_pass[8:-16],orig_pass[-16:]

def flip_bit(i,byte_string):
    """flip ith bit from the end"""
    mask =  (1<<(i)).to_bytes(42,'big')
    return pwn.xor(byte_string,mask)

def try_decryption(password:bytes):
    REM = pwn.process("ncat --ssl 7b0000008e9e58b1a57d85e4-secure-flag-service.challenge.master.allesctf.net 31337",shell=True)
    REM.sendline(base64.b64encode(password))
    data = REM.recvline().split(b'password>')[-1]
    REM.close()
    if b'Get off my lawn' not in data:
        return data
    return False

recovered_password = 0
for i in range(21*8):
    pass1 = flip_bit(2*i,orig_pass)
    pass2 = flip_bit(2*i+1,orig_pass)
    val1 = try_decryption(nonce+pass1+tag)
    if val1:
        recovered_password |= (1<<i)
    else:
        val2 = try_decryption(nonce+pass2+tag)
        if val2:
            recovered_password |= (1<<i)
    print(recovered_password.to_bytes(21,'big'))

PASSWORD = recovered_password.to_bytes(21,'big')
# PASSWORD = b'kldsjvd!!!##130983575'
encryption_key = BLAKE2s.new(data=PASSWORD + b'encryption_key').digest()
mac_key = BLAKE2s.new(data=PASSWORD + b'mac_key').digest()
encrypted_flag = try_decryption(nonce+orig_pass+tag)
print(decrypt(base64.b64decode(encrypted_flag)))





