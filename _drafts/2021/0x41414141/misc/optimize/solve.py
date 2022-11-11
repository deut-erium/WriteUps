from pwn import remote, context
import re
HOST, PORT = "207.180.200.166", 9660


context(log_level=0)
REM = remote(HOST,PORT)

def inv_count(arr): 
    inv_count = 0
    for i in range(len(arr)): 
        for j in range(i + 1, len(arr)): 
            if arr[i] > arr[j]: 
                inv_count += 1
    return str(inv_count).encode()

for _ in range(25):
    chall = REM.recvuntil(b'>')
    REM.sendline(  str(2**(chall.count(b',')+1)-1).encode())

for _ in range(25):
    chall = REM.recvuntil(b'>')
    arr = eval(re.search(b'\[.*\]',chall)[0])
    REM.sendline( inv_count(arr) )
    
REM.interactive()

