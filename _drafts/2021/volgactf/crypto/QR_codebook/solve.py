from PIL import Image
from pwn import xor
qr = Image.open('qr.png').convert('RGB')
qr_enc = Image.open('qr.encrypted.png')
flag_enc = Image.open('flag.encrypted.png')

qr_data = list(qr.getdata())
qr_enc_data = list(qr_enc.getdata())
flag_enc_data = list(flag_enc.getdata())

w,h = qr.size
qr_rows = [qr_data[w*i][0] for i in range(h)]
qr_enc_rows = [qr_enc_data[w*i][0] for i in range(h)]


qr_mask = xor(bytes(qr_rows),bytes(qr_enc_rows))
qr_mask = qr_mask+qr_mask
w,h = flag_enc.size
flag_enc_rows = bytes([flag_enc_data[w*i][0] for i in range(h)])
flag = Image.new(size=(w,h),mode='1')

flag_enc_pixels = [ i[0] for i in flag_enc_data ]
for i in range(w):
    for j in range(h):
        flag_enc_pixels[w*i+j]^=qr_mask[i]

flag.putdata(flag_enc_pixels)

#flag.putdata(xor(flag_enc_pixels,qr_mask))
#mask_tentative = [0]*7+[0xff]+[0]+[0xff]*6+[0]*4+[0xff]+[0]+[0xff]+[0]*7
#mask = []
#l=int(w/29)
#for i in mask_tentative:
#    if i==0:
#        mask.extend([0]*l)
#    else:
#        mask.extend([0xff]*l)
#mask = bytes(mask+[0,0])
#enc_key = xor(flag_enc_rows,mask)

for j in range(w):
    for i in range(h):
        pixel = flag_enc.getpixel((i,j))[0]^qr_mask[i]
        flag.putpixel((i,j),(pixel,)*3)
#

