from pwn import xor, remote

HOST, PORT = "2022.ductf.dev", 30009

REM = remote(HOST, PORT)

message = b'Decrypt this... '

IV = bytes(16)

REM.recvuntil(b"iv: ")
REM.sendline(IV.hex())
encrypted1 = bytes.fromhex(REM.recvline().strip().decode())
E_iv = xor(message, encrypted1[:16])
REM.recvuntil(b"iv: ")
REM.sendline(E_iv.hex())
encrypted2 = bytes.fromhex(REM.recvline().strip().decode())

messages = [message]

for i in range(0,len(encrypted1)-16,16):
    enc_iv = xor(encrypted2[i:i+16], messages[-1])
    new_mess = xor(encrypted1[i+16:i+32], enc_iv)
    messages.append(new_mess)

print(b"".join(messages))




