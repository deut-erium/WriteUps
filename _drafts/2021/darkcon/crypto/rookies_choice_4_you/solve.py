from pwn import xor
ct = bytes.fromhex('3d5d841c4df203758189060d7ba5ef0460c90faeae890dc621dfb563a03cc5f728d42794ae8a08102f2766acece427f3c6514fc7')
key = xor(ct,b'abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz')

flag = bytes.fromhex('385e95136bdb2a66baa0593e27b8df03228f1785ea9925c768d08b74b06bffe27bd17da1aed51c21342026bdacb173f8')
print(xor(flag,key))
b'darkCON{RC4_1s_w34k_1f_y0u_us3_s4m3_k3y_tw1c3!!}\x89w\xa3\xae'
