from sympy.crypto.crypto import encipher_hill,decipher_hill
import string
from sympy import Matrix
from pwn import remote,context

context(log_level=0)

CHARSET = string.ascii_lowercase
HOST, PORT = "chall.nitdgplug.org",30211
REM = remote(HOST,PORT)

while True:
    REM.recvline()
    key = REM.recvline().strip().split(b': ')[-1].decode()
    ct = REM.recvline().strip().split(b': ')[-1].decode()
    key_int = [CHARSET.index(i) for i in key]
    n = int(len(key)**0.5)
    key_mat = Matrix([ [key_int[j*n+i] for i in range(n)] for j in range(n)])
    pt = decipher_hill(ct,key_mat,symbols=CHARSET)
    REM.sendline(pt)

#GLUG{17_15_34513r_70_g0_d0wn_4_h1ll_7h4n_up_bu7_7h3_v13w _15_fr0m_7h3_70p}
