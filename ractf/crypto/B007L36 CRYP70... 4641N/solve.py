from pwn import remote
from base64 import b64decode as d64
from base64 import b64encode as e64

HOST, PORT = "95.216.233.106", 60246

with open('password.txt','r') as password_file:
    password = d64(password_file.read().strip()).decode()

with open('ciphertext.txt','r') as ciphertext_file:
    ct = d64(ciphertext_file.read().strip()).decode()

with open('plaintext.txt', 'r') as plaintext_file:
    pt = plaintext_file.read().strip()

REM = remote(HOST, PORT)
print(REM.recvline())
print(REM.recvline())

def encrypt(pt, key):
    REM.recvuntil(b'data with:')
    REM.sendline(key)
    REM.sendline(pt)
    data = REM.recvuntil(b'\n\n')
    encrypted = data.split(b'message is: ')[-1].strip()
    return [ord(i) for i in d64(encrypted).decode()]

ct_arr = [ord(i) for i in ct]
pt_arr = [ord(i) for i in pt]

diff_arr = [ct_arr[i] - pt_arr[i] for i in range(len(ct_arr))]

print("".join(chr(i) for i in diff_arr))

key = "ractf{n0t_th3_fl49_y3t}"


# ractf{n0t_th3_fl49_y3t}ractf{n0t_th3_fl49_y3t}ractf{n0t_th3_fl49_y3t}ractf{n0t_th3_fl49_y3t}ractf{n0t_th3_fl49_y3t}ractf{n0t_th3_fl49_y3t}ra

flag = "".join( chr(ord(password[i]) - ord(key[i%len(key)])) for i in range(len(password)) )
print(flag)
