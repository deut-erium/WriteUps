import pwn

REM = pwn.process('python3 main.py',shell=True)
# REM = pwn.remote('ctf.k3rn3l4rmy.com',2234)

def f(l,k):
    REM.sendline(str(k))
    REM.sendline(str(l))
    data = REM.recvuntil(b'\n\n')
    return int(data.split(b' = ')[-1].strip())

l = 1
k = 2**513
i=0
while l.bit_length()<512:
    l+=f(l,k)
    i+=1
    print(i,l)
N = f(l,k)-l
for _ in range(600-i-1):
    assert f(N,N)==N
REM.sendline(str(N))
REM.interactive()

#flag{h4cking_th3_GCD!}
