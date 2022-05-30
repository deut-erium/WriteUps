coords = [(9,10),(4,1),(3,4),(3,9),(3,1),(2,4),(8,4),(8,1),(1,2),(9,5),(2,2),(5,7),(7,4),(9,8),(5,9),(7,8),(4,6),(1,3),(2,5),(5,8),(1,8),(9,1),(8,9),(1,5),(8,8),(2,6),(8,7),(7,2),(5,4),(6,4),(6,1),(7,5),(1,6),(8,5),(5,6),(9,2),(1,7),(2,10),(2,7),(2,1),(6,6),(2,8),(3,2),(9,9),(3,7),(6,3),(4,8),(2,3),(6,10),(5,1),(7,7),(4,7),(7,3),(6,9),(5,2),(3,8),(8,10),(3,3),(7,10),(9,6),(5,3),(8,3),(9,4),(6,7),(9,7),(6,2),(8,2),(1,1),(1,9),(6,8),(7,1),(4,10),(3,10),(6,5),(4,2),(5,10),(1,10),(4,9),(4,3),(8,6),(1,4),(7,6),(5,5),(4,5),(9,3),(4,4),(2,9),(7,9),(3,5),(3,6)]

import os
img_list = sorted(os.listdir('pieces'))
from PIL import Image

images_data = [ list(Image.open('pieces/'+i).getdata()) for i in img_list]

# out_img = Image.new(mode='RGB',size=(100*9,10*10))


# for img_pix,(X,Y) in zip(images_data,coords):
#     oX,oY = (X-1)*100, (Y-1)*10
#     for i in range(100):
#         for j in range(10):
#             out_img.putpixel( (oX+i, oY+j), img_pix[100*j+i])
out_img = Image.new(mode='RGB',size=(100*10,10*9))


for img_pix,(X,Y) in zip(images_data,coords):
    oX,oY = (Y-1)*100, (X-1)*10
    for i in range(100):
        for j in range(10):
            out_img.putpixel( (oX+i, oY+j), img_pix[100*j+i])
