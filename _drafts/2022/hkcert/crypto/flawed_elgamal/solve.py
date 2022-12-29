from pwn import remote
from math import gcd

c2s = []

for _ in range(100):
    HOST, PORT = "chal.hkcert22.pwnable.hk", 28021
    REM = remote(HOST, PORT)

    c1 = int(REM.recvline().strip().split()[-1])
    c2 = int(REM.recvline().strip().split()[-1])
    c2s.append(c2)
    m_tent = gcd(*c2s)
    print(m_tent.to_bytes((m_tent.bit_length()+7)//8,'big'))
    REM.close()

#hkcert22{4nd_th1s_t1m3_7h3_i5su3_1s_s0l31y_n0t_t4k1n9_m0du10s}
