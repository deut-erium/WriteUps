from PIL import Image
from Crypto.Util.number import bytes_to_long, long_to_bytes
from Crypto.Cipher import AES

IV_ORIG = b'ASDFQWER'


k = b'\x10\x82u\x98:\x1c\x0fy\x10/4{\xd8\xc3\xa9u\xe3x\x8a\x9d3ru\xc1\x93\xf5i\x8c6\xdf\x15\x01'
iv = iv = b'\xbb\x9c\xe2\x8d\xd0\xd1\xbe@\xf6l\x02\xc95\x15\x1cF'

key = b'_D3f1nItEly_giV3_IT_@_Sh0T_th1s_Is_n0T_4rT_BuT_th3_3aRt_0f_m3kD4d_sH1Li_'

key = bytes_to_long(key)

im = Image.open('brain_memory.png')
ffmok_pixels = [None for _ in range(887*22)]
itr = 0
for y in range(887):
    for x in range(22):
        ffmok_pixels[itr] = im.getpixel((y,x))
        itr+=1

ffmok_bytes,ffmok_pixels = ffmok_pixels[:4],ffmok_pixels[4:]

ffmok_bytes = []
for i in range(0,len(ffmok_pixels),2):
    r1,g1,b1,o1 = 

