from net import *
import numpy as np
import scipy.optimize as opt

model = torch.load("model.pth",map_location=torch.device("cpu"))

def save_np(h,w):
    with open(f'test_{h}x{w}.npy','wb') as f:
        np.save(f,np.ones((h,w)))

TARGET = np.array([0.0470, 0.9530])

def objective(np_arr):
    target = TARGET
    np_arr = np_arr.astype('float32')
    value = model.forward(torch.from_numpy(np_arr.reshape(1,1,224,224)))
    value = value.detach().numpy()[0]
    return np.linalg.norm(target-value)

x_init = np.zeros(224*224,dtype='float32')

with open('final.npy', 'wb') as f:
    np.save(f, -6.943*np.ones((224,224)))

#HTB{b3nd1ng_th3_0utput_t0_y0ur_w1LL}
