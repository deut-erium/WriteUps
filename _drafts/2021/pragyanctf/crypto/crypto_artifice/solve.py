from PIL import Image
from pwn import xor


def long_to_bytes(x):
    return int.to_bytes(x,(x.bit_length()+7)//8,'big')

im1 = Image.open('pic1.png')
im2 = Image.open('pic2.png')

x,y = im1.size
color = lambda x,y,z: (255,255,255) if x else (0,0,0)
im_new = Image.new(mode='RGB',size=(x//2,y))
im_new2 = Image.new(mode='RGB',size=(x//2,y))


for i in range(x//2):
    for j in range(y):
        r1,g1,b1 = im1.getpixel((i,j))
        r2,g2,b2 = im1.getpixel((x-i-1,j))
        new_pixel = ((r2^r1)%256, (g2^g1)%256, (b2^b1)%256)
        im_new.putpixel((i,j),color(*new_pixel) )

for i in range(x//2):
    for j in range(y):
        r1,g1,b1 = im2.getpixel((i,j))
        r2,g2,b2 = im2.getpixel((x-i-1,j))
        new_pixel = ((r2^r1)%256, (g2^g1)%256, (b2^b1)%256)
        im_new2.putpixel((i,j),color(*new_pixel) )

im_new.show()
im_new2.show()

B_public = 6193911118
p = 6971096459
g = 2
secret1 = bytes.fromhex('075f5d6e0140056843036c5c4c52586b56425e4e')
B_priv = 876543224 
A_public = 5030649929
secret2 = bytes.fromhex('436e5a45564f43065d435f48664900466f06446c')
A_priv = 456789639
shared_sec = str(pow(B_public,A_priv,p)).encode()
print(xor(secret2,shared_sec)+xor(secret1,shared_sec))
#p_ctf{s1mply_x0r_1t_4nd_1t5_s0_much_fun}
