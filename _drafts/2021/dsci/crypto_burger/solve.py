from PIL import Image

img1 = Image.open('Burger_Bun_Bottom.png')
img2 = Image.open('Burger_Bun_Top.png')

img3 = Image.new(img1.mode, img1.size)
data1 = img1.getdata()
data2 = img2.getdata()
# data3 = [lambda a,b: 0 if (a==0 and b==0) or (a==255 and b==255) else 255 for i,j in zip(data1,data2)]
data3 = [0 if (a==0 and b==0) or (a==255 and b==255) else 255 for a,b in zip(data1,data2)]
img3.putdata(data3)
