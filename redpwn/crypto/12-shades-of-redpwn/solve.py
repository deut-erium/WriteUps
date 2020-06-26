EXTRACTED = '86 90 81 87 a3 49 99 43 97 97 41 92 49 7b 41 97 7b 44 92 7b 44 96 98 a5'

flag = ''.join([chr(int(i,12)) for i in EXTRACTED.split()])
print(flag)
