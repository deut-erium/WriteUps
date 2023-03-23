import torch
from torch import nn
import numpy as np

def StarChartModel(dropout=[0.0,0.0], out_classes=2):
    model = nn.Sequential(
        nn.Conv2d(3, 8, (3,3), padding='same'),
        nn.ReLU(),
        nn.Conv2d(8, 16, (3,3), padding='same'),
        nn.ReLU(),
        nn.MaxPool2d((4,4)),
        nn.Flatten(),
        nn.Dropout(dropout[0]),
        nn.Linear(4624, 256),
        nn.ReLU(),
        nn.Dropout(dropout[1]),
        nn.Linear(256, 128),
        nn.ReLU(),
        nn.Linear(128, out_classes),
        nn.Softmax(dim=1)
    )
    return model

one_hot = torch.tensor(np.identity(2), dtype=torch.float32)

class StarData(torch.utils.data.Dataset):
    def __init__(self, set_X, set_Y, transform = None):
        self.transform = transform
        self.X = set_X
        self.Y = set_Y
        
    def __len__(self):
        return len(self.X)
    
    def __getitem__(self, idx):
        x = self.X[idx]
        target_class = self.Y[idx]
        y = one_hot[target_class]
        if self.transform:
            return self.transform(torch.tensor(x).float()), y, target_class
        return torch.tensor(x).float(), y, target_class