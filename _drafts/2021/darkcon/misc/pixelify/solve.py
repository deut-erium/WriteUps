
import base64
from PIL import Image

IMG = Image.open("inject.png")
colours = [
            (255, 0, 0),
            (0, 0, 255),
            (0, 128, 0),
            (255, 255, 0)
        ]

data = list(IMG.getdata())
enc = []
for i in range(0,len(data),4):
    v = 0
    if data[i]==(0,0,0):
        break
    for j in range(4):
        v*=4
        v += colours.index(data[i+j])
    enc.append(chr(v))


bin_data = base64.b64decode("".join(enc))
with open('inject.bin','wb') as f:
    f.write( bin_data )



