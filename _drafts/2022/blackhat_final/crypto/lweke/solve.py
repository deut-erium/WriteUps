import pwn
import base64
from lweke import dec_mat

REM=pwn.process("python3.11 lweke.py",shell=True)
data = REM.recvuntil(b"Send me your public key for a handshake\n")

pub_encoded = pwn.re.search(b"M = (.*)\n\|\n\|",data)[1]
M = dec_mat(pub_encoded)

FLAG_ENC  = pwn.re.search(b"F = (.*)\n",data)[1]
FLAG_ENC = bytes.fromhex(FLAG_ENC.decode())
