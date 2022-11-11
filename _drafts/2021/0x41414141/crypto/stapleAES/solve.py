from pwn import remote, xor

HOST,PORT = "161.97.176.150", 3167

#a^pt1 , b^ pt2, c^pt3



cts = set()
while len(cts)<6:
    REM = remote(HOST,PORT)
    data = bytes.fromhex(REM.recvline().strip().decode())
    cts.add(data)
    REM.close()

cts = list(set(cts))

#flag{I_7h0ught_7h1s_wa5_@_s3cr3t}
