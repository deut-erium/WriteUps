import pwn
from hashlib import sha256
from itertools import product
HOST, PORT = "asr.2021.3k.ctf.to", 13371
REM = pwn.remote(HOST,PORT)
data = REM.recvuntil(b'Answer: ')
prefix = pwn.re.search(b'\'(\w+)\'',data)[1]

for s in product(range(0x20,0x7f),repeat=6):
    if sha256(prefix+bytes(s)).digest().startswith(b'\x00'*3):
        print(bytes(s))
        break

REM.sendline(bytes(s))

key = b'''-----BEGIN RSA PRIVATE KEY-----
MIIDcAIBAAKBoh1xC9SK3iwX2oK16ANCROwcz2EHpk9EvNbfph/XZ3qMJYGZO4cC
pbodDvcqkeFldCEdythioJk2pnPqZH0uakNoYZlSey9UeXr+6pCcY48og/DuxGve
Lh3S7MpfkksjDt7e8PJ90D1LJ2U2aowmgMMaNxJKHh8hYJzNZybjAis3ZsajnGkc
loaX3C5JpmFjYQ4vhIY2ro5KAl4PhK4kJvPvSQKBohcN6ee+SMd6qal5qL88mKRB
frZXR9Ljgdj7P3+r3201iJNQ1UV/N79ZlgAk8EToh2fNR0CGIS9neGJVztBiN4ib
KjeWnX1SmRDGsEblV7IDXAR1bNuD3rN3ptOorrQwr+jdaVxEZg+KtvYw99Kw50fr
bh1+LsWLMlSLSAFWSuZwsrzFXOx/vf9DqhjdF9CDGI7nOX6tUwmhzelLXT6lrzPZ
awKBogdxCCfJP7QUCKB2/Dcv5b7ji4YxzYg3VbDAHr1VNuNWq3zbtUfUm2C2TurZ
4L+pgGF6YVv/hM7FOryytIlzVVZEDyOD6VXdxK/Z0qdONfzfWpjbgc5cIxE6/MLh
cOQwmqiLQ7bXK5+rH43xrQDwqKZk0svdPVHxpKcLKQ2j6GoHeM8sn+KHDwds0gK2
e1H91Lx1mhQWX616djRmtUUB0C5E5wIuAWPO5V1VXAb/5qaq2qZQ/r6Zx2Mc3yRO
iNOVGny/qu6DCpvX09rfEek9uOvEywJ1FS7R+X2ftJqmM+neYmdGzrRUiryw08ih
THwH5Gnp0cj0mUKEdBcsk5DtsRx2oKRC+k0FEFwPvkanv37Q9vGKNYeygKc5TwJh
20pHwmznH8tS6JnvjjA1ifJTXPZO3RH2nGZIVGptiszTEtnuAoAsG8gieq27Ai4B
SYiR5u5Mh6TAoHaImoa6DHfrSlEVgMstLYOFCjfDCqfG4zWDroc1azNtZaqzAnUU
YKs086XSQwlqpUUeSy4KEGKjJgBNf97c6PlK0tTx/gfrqh02tUxfe8HCVWByFA1I
0E6i9W/9qCclonjzZudH0vn29ZunjUUTG/1PzGDn4t8S4oIwnBPeoJmQCft0sYkA
H8IsPJRrjQrb2+epuwzyxixnwNMCLgFgQWvMDqcvY0+9z1lqvgxk4WNKy/HsgO0N
fSRNk+Kmwfniok46LtPVi9sM5z4=
-----END RSA PRIVATE KEY-----'''
#for key_frag in key:
#    REM.send(key_frag)
REM.sendline(key)
REM.interactive()
#3k{d1scr3t3_l0g__1sNt__h4rD???}
