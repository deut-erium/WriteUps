import pwn
from Crypto.Cipher import AES

REM = pwn.remote("flipmeover.chall.cryptonite.team", 1337)

def gettoken(username:bytes):
    REM.sendline(username.hex())
    data = REM.recvuntil(b'Enter token in hex():')
    hexa = pwn.re.search(b'([0-9a-f]+)\n',data)[1]
    tag, ct = hexa[:32], hexa[32:]
    return tag,ct

tag,ct = gettoken(b'\x00'*16)
REM.sendline(b'0'*64)
REM.sendline(b'0'*32)
targetpt = b'gimmeflag_______'

data = REM.recvuntil(b'Enter token in hex():')
bs_plus_dec_0 = pwn.re.search(b'([0-9a-f]+)\n',data)[1]
bs, dec_0 = bs_plus_dec_0[:32], bs_plus_dec_0[32:]
c2 = pwn.xor(bytes.fromhex(dec_0.decode()),targetpt)
c2 = c2.hex()
REM.sendline(c2+'0'*32)
REM.sendline(b'0'*32)
REM.interactive()
#nite{flippity_floppity_congrats_you're_a_nerd}

