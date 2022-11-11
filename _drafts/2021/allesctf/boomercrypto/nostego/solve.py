from PIL import Image
from tqdm import tqdm
import pickle
import os
import z3
from z3 import BitVec, ZeroExt
from collections import Counter

enc_file = "ALLES.enc.png"
# enc_file = "test_img.enc.png"
image = Image.open(enc_file).convert("F")
width, height = image.size
result = Image.new("F",(width,height))
ROUNDS = 32

# original_image = [BitVec(f'img[{i//width}][{i%width}]',8) for i in range(width*height)]

original_image = [[BitVec(f'img[{i}][{j}]',8) for i in range(height)] for j in range(width)]



if os.path.exists(enc_file+'image_sum.pickle'):
    print('loaded')
    with open(enc_file+'image_sum.pickle','rb') as f:
        result_sums = pickle.load(f)
else:
    result_sums = [[0 for _ in range(width)] for _ in range(height)]
    for i in range(width):
        for j in range(height):
            result_sums[i][j] = int(image.getpixel((i,j))*ROUNDS)
    with open(enc_file+'image_sum.pickle','wb') as f:
        pickle.dump(result_sums,f)

constraints = []
indices = []
index_count = Counter()
for i in tqdm(range(width)):
    for j in range(height):
        value = 0
        index_values = []
        di, dj = 1337, 42
        for k in range(ROUNDS):
            di, dj = (di * di + dj) % width, (dj * dj + di) % height
            x,y = (i+di)%width, (j+dj + (i+di)//width)%height
            # pixel = original_image[x*width + y]
            # pixel = original_image[x][y]
            # value += ZeroExt(ROUNDS.bit_length()+1,pixel)
            index_values.append((x,y))
            index_count[x+512*y]+=1
        indices.append(index_values)
            # value.add( ((i+di)%width, (j+dj+(i+di)//width)%height ))
        # constraints.append(value==result_sums[i][j])

            # value += ZeroExt(5,original_image[(i + di) % width][(j + dj + (i + di)//width) % height])
        # constraints.append(value==result_sums[i][j])

# s = z3.Solver()
# s.add(constraints)
# if s.check()==z3.sat:
#     print("sat")
#     m = s.model()




