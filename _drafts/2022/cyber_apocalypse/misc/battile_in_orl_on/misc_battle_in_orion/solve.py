from net import *
import numpy as np

model = torch.load("model.pth",map_location=torch.device("cpu"))

def save_np(h,w):
    with open(f'test_{h}x{w}.npy','wb') as f:
        np.save(f,np.ones((h,w)))

with open('final.npy', 'wb') as f:
    np.save(f, -6.943*np.ones((224,224)))

#HTB{b3nd1ng_th3_0utput_t0_y0ur_w1LL}
