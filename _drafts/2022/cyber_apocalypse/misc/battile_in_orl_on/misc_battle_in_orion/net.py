import torch
import torch.nn as nn

class net(nn.Module):
    def __init__(self):
        super(net,self).__init__()
        
        self.layer1 = nn.Sequential(
            nn.Conv2d(1,16,kernel_size=3,padding=0,stride=2),
            nn.ReLU(),
            nn.MaxPool2d(2)
        )
        
        self.layer2 = nn.Sequential(
            nn.Conv2d(16,32,kernel_size=3,padding=0,stride=2),
            nn.ReLU(),
            nn.MaxPool2d(2)
        )
        
        self.fc1 = nn.Linear(5408,10)
        self.fc2 = nn.Linear(10,2)
        self.relu = nn.ReLU()
        
    def forward(self,x):
        out = self.layer1(x)
        out = self.layer2(out)
        out = out.view(out.size(0),-1)
        out = self.relu(self.fc1(out))
        out = self.fc2(out)
        out = torch.softmax(out, dim=1)
        return out