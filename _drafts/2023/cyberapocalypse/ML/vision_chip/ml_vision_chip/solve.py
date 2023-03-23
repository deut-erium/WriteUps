import numpy as np
import matplotlib.pyplot as plt
import matplotlib

import torch
from PIL import Image
from torchvision import transforms

preprocess = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

from model import EarthVisionModel

def unpickle(file):
    import pickle
    with open(file, 'rb') as fo:
        _dict = pickle.load(fo, encoding='bytes')
    return _dict

label_meta = unpickle("./meta")

model = EarthVisionModel()
model.load_state_dict(torch.load("state_dict.pt"))

model.eval()

def eval_img(img_path):
    img = Image.open(img_path)
    img_tensor = preprocess(img)
    img_tensor = img_tensor.unsqueeze(0)
    with torch.no_grad():
        output = model(img_tensor)
        prediction = torch.argmax(output, dim=1).item()
    label = label_meta[b'fine_label_names'][prediction]
    return label

flag = np.zeros((32,256))
from tqdm import tqdm
preds = {}
for i in tqdm(range(8192)):
    preds[i] = eval_img(f"test_X/{i}.jpg")
    if preds[i] in label_meta[b'label_map'][b'large_man-made_outdoor_things']:
        flag[i//256,i%256] = 1

plt.imshow(flag,cmap='gray')
plt.show()

