import os
KEY = os.urandom(27)
print(KEY)
KEY = KEY.hex()
FLAG = (b'X'*100).hex()
