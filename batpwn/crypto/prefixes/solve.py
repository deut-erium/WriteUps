ct = "eae4a5b1aad7964ec9f1f0bff0229cf1a11b22b11bfefecc9922aaf4bff0dd3c88"

ct = bytes.fromhex(ct)

flag = ""

initialize = 0
for i in range(len(ct)):
    for val in range(256):
        if (initialize ^ (val<<2)^val)&0xff == ct[i]:
            flag += chr(val)
            initialize ^= (val<<2)^val
            initialize >>=8
            break
print(flag)
#batpwn{Ch00se_y0uR_pR3fix_w1selY}
