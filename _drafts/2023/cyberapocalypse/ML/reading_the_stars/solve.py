
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import os
from PIL import Image

import torch
from torch import nn
from torchvision import transforms
preprocess = transforms.Compose([
    transforms.Normalize(
        mean=np.array([0.1086, 0.0934, 0.0711]),
        std=np.array([0.1472, 0.123, 0.1032]))
])

import h5py

SEED = 1337
torch.manual_seed(SEED)
np.random.seed(SEED)
torch.use_deterministic_algorithms(True)

from model import StarChartModel, StarData

with h5py.File("train.1.h5", "r") as F:
    train_images1 = np.array(F["X"])
    train_labels1 = np.array(F["y"])
with h5py.File("train.2.h5", "r") as F:
    train_images2 = np.array(F["X"])
    train_labels2 = np.array(F["y"])

train_images = np.concatenate((train_images1, train_images2))
train_labels = np.concatenate((train_labels1, train_labels2))

batch_size = 32
train_set = StarData((train_images.transpose(0,3,1,2)/255), train_labels, transform=preprocess)
train_loader = torch.utils.data.DataLoader(train_set, batch_size=batch_size,
    shuffle=True, num_workers=1, pin_memory=True)

model = StarChartModel([0.3,0.15])
model.train()

loss_func = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), 0.0005)

with h5py.File("test.h5","r") as F:
    test_images_raw = np.array(F["X"],dtype=np.int8)

test_images = test_images_raw.transpose(0, 1, 2, 5, 3, 4)/255  # (33, 33, 2, 3, 69, 69)
test_images = test_images.reshape(-1,3, 69, 69)  # (33*33*2, 3, 69, 69)

# Preprocess the test_images array
test_images = torch.tensor(test_images).float()
test_images = preprocess(test_images)

MODEL_FILE_NAME = "model_state_dict.pt"

if os.path.exists(MODEL_FILE_NAME):
    model.load_state_dict(torch.load(MODEL_FILE_NAME))
else:
    num_epochs,log_interval = 200,100
    for epoch in range(num_epochs):
        running_loss = 0.0
        for i, data in enumerate(train_loader, 0):
            inputs, labels, target_class = data
            optimizer.zero_grad()
            outputs = model(inputs)
            loss = loss_func(outputs, torch.argmax(labels, dim=1))
            # loss = loss_func(outputs, target_class)
            loss.backward()
            optimizer.step()
            running_loss += loss.item()
        print(f"Epoch {epoch+1}, loss: {running_loss/(i+1)}")
        if epoch%5==0:
            model.eval()
            with torch.no_grad():
                output = model(test_images)
                predicted_classes = torch.argmax(output, dim=1).reshape(33, 33, 2).numpy()
                p0 = predicted_classes[:,:,0]
                p1 = predicted_classes[:,:,1]
                print("num differing =", sum(sum(p0^p1)))
            model.train()
            torch.save(model.state_dict(), MODEL_FILE_NAME)



# Make predictions
model.eval()
with torch.no_grad():
    output = model(test_images)
    predicted_classes = torch.argmax(output, dim=1).reshape(33, 33, 2).numpy()


p0 = predicted_classes[:,:,0]
p1 = predicted_classes[:,:,1]

mask = np.zeros((33,33),dtype=int)
mask_img = Image.open("mask.png")

def apply_mask(img):
    res = img.copy()
    for i in range(33):
        for j in range(33):
            x = mask_img.getpixel((i,j))
            if x==(255,255,255):
                res[i,j] = 1
            elif x==(0,0,0):
                res[i,j] = 0
    return res

from pyzbar.pyzbar import decode
print("num differing =", sum(sum(p0^p1)))
print(decode(p0))
print(decode(p1))
print(decode(apply_mask(p0)))
print(decode(apply_mask(p1)))
print(decode(apply_mask(p0|p1)))
print(decode(apply_mask(p0&p1)))
plt.imshow(p0,cmap='gray')
plt.show()
plt.imshow(p1,cmap='gray')
plt.show()
plt.imshow(apply_mask(p0),cmap='gray')
plt.show()
plt.imshow(apply_mask(p1),cmap='gray')
plt.show()

