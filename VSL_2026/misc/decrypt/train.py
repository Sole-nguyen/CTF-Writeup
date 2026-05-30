import torch
import torch.nn as nn

data = list(range(32,127))

with open('label.txt','rb') as f:
    label = [i-32 for i in f.read()]

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

##model = MyNet()
model = torch.load('model',weights_only=False)

optim = torch.optim.Adam(model.parameters(), lr = 0.00001)
loss = nn.NLLLoss()

print('training')

model.train()
for epoch in range(5000):
    in_d = torch.Tensor([[float(data[i])] for i in range(95)])
    out_d = torch.tensor([label[i] for i in range(95)],dtype=torch.int64)
    optim.zero_grad()
    pred = model(in_d)
    pred_loss = loss(pred, out_d)
    pred_loss.backward()
    optim.step()
    if epoch % 100 == 0:
        print(f'epoch {epoch}; loss: {pred_loss.item()}')

model.train(False)
torch.save(model, 'model')
