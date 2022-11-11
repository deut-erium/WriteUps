import pwn
from tqdm import tqdm
HOST, PORT = "gc1.eng.run" , 30092
REM = pwn.remote(HOST, PORT)

def get_enc(data:bytes):
    REM.sendline(data.hex())
    recvd = REM.recvuntil(b'\x1b[0m')
    print(recvd)
    if b'ErrorOccured' in recvd:
        print("what!!!!!!!!!!!!!!!!")
    # return b'Invalid Padding' not in recvd
    return b'Successfully Decrypted' in recvd

FLAG_ENC = bytes.fromhex('b573a096bf6f525498eb19d297eb95e534fd997eb03ba2a1259a22f2d4d9e4a421d6765fb3c5e26fe5aa2ba8448aa06ac229ae5e0292d3544951027ce8acb47f')
IV = bytes.fromhex('28381f47d0097c7765468968179a722e')

BLOCK_SIZE = 16


def single_block_attack(block, oracle,last_block):
    zeroing_iv = [0] * BLOCK_SIZE
    for pad_val in range(1, BLOCK_SIZE+1):
        padding_iv = [pad_val ^ b for b in zeroing_iv]
        for candidate in tqdm(range(256)):
            padding_iv[-pad_val] = candidate
            iv = bytes(padding_iv)
            if oracle(iv+block):
                if pad_val == 1:
                    # padding_iv[-2] ^= 1
                    # iv = bytes(padding_iv)
                    # if not oracle(iv+block):
                        print("false positive??")
                        # continue  # false positive; keep searching
                break
        else:
            raise Exception("no valid padding byte found (is the oracle working correctly?)")
        zeroing_iv[-pad_val] = candidate ^ pad_val
    print(bytes(zeroing_iv))
    print(pwn.xor(zeroing_iv,last_block))
    return zeroing_iv


def full_attack(iv, ct, oracle):
    """Given the iv, ciphertext, and a padding oracle, finds and returns the plaintext"""
    assert len(iv) == BLOCK_SIZE and len(ct) % BLOCK_SIZE == 0
    msg = iv + ct
    blocks = [msg[i:i+BLOCK_SIZE] for i in range(0, len(msg), BLOCK_SIZE)]
    result = b''
    iv = blocks[0]
    prefix = b''
    for ct in blocks[1:]:
        dec = single_block_attack(ct, oracle,prefix)
        pt = bytes(iv_byte ^ dec_byte for iv_byte, dec_byte in zip(iv, dec))
        result += pt
        print(result)
        print('here')
        prefix+=ct
        iv = ct
    return result

# full_attack(IV,FLAG_ENC, get_enc)
# full_attack(FLAG_ENC[:16],FLAG_ENC[16:], get_enc)

