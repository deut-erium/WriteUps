send public key 1

key = hashlib.md5(long_to_bytes(1)).digest()
cipher = AES.new(key,AES.MODE_ECB)
cipher.encrypt( b"Initialization Sequence - Code 0").hex()
7fd4794e77290bf65808e95467f284966d71995c16e83da2192aecfd2d0df7a4
# HTB{7h15_p2070c0l_15_pr0tec73d_8y_D@nb3er_c0pyr1gh7_1aws}
