import torch
import torch.nn as nn
from secret import flag

class MyNet(nn.Module):
    def __init__(self):
        super().__init__()
        self.linear1 = nn.Linear(1, 512)
        self.linear2 = nn.Linear(512, 2048)
        self.linear3 = nn.Linear(2048, 1024)
        self.linear4 = nn.Linear(1024, 95)
        self.active = nn.ReLU()
        self.reg = nn.LogSoftmax(dim=1)
    def forward(self, x):
        x = self.active(self.linear1(x))
        x = self.active(self.linear2(x))
        x = self.active(self.linear3(x))
        x = self.reg(self.linear4(x))
        return x

model = torch.load('model',weights_only=False)
flag = torch.Tensor([[float(i)] for i in flag])

with open('output.txt','w') as f:
    a = model(flag)
    f.write(bytes([i+32 for i in a.argmax(dim=1).tolist()]).decode())


