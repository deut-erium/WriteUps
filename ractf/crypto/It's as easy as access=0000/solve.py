from pwn import remote, xor
import json

HOST, PORT = "95.216.233.106", 58891

REM = remote(HOST, PORT)
print(REM.recvuntil(b'Your choice: ').decode())

REM.sendline(b'1')  #get a guest token
data = REM.recvline().replace(b"'",b'"') # badly formatted json
token = json.loads(data)['token']

admin_token = token[32:] # first 32 is iv
iv = bytes.fromhex(token[:32])
iv_xor = b'\x00'*7 + xor(b'9','0')*4 + b'\x00'*5
iv_for_admin = xor(iv_xor, iv).hex()


REM.sendline(b'2')
REM.sendline(admin_token.encode())
REM.sendline(iv_for_admin.encode())
print(REM.recvlines(4))

# ractf{cbc_b17_fl1pp1n6_F7W!}

