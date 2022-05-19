import pwn

HOST, PORT = "crypto.hsctf.com", 6001
rem = pwn.remote(HOST, PORT)

rem.recvline()
data = rem.recvline()

def nextval(num):
    return (num*0x25 + 0x41)&0xff

initial = data.decode().strip().split(':')[-1]
print(initial)
initial = int(initial)

for i in range(10):
    rem.sendline(str(nextval(initial)).encode())
    print(rem.recvline().decode())
    initial = nextval(initial)
