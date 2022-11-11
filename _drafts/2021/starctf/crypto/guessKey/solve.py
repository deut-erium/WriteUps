from pwn import remote
HOST, PORT = "52.163.228.53", 8080
REM = remote(HOST,PORT)
key = REM.recvline()
for i in range(3):
    REM.sendline(b'0')
    REM.send(key)
REM.interactive()
REM.close()
#*CTF{bcceb9d0913793c7d10ffedddac47cd2}