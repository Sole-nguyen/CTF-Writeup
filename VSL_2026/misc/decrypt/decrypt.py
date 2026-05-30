import torch
import torch.nn as nn

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

# Load the model
model = torch.load('model', weights_only=False)
model.eval()

# Read encrypted text
with open('output.txt', 'r') as f:
    encrypted = f.read().strip()

print(f"Encrypted text: {encrypted}")

# Build the mapping: for each possible input (32-126), find what output it produces
encryption_map = {}
for i in range(32, 127):  # ASCII printable characters
    input_tensor = torch.Tensor([[float(i)]])
    output = model(input_tensor)
    encrypted_char_value = output.argmax(dim=1).item() + 32
    encrypted_char = chr(encrypted_char_value)
    encryption_map[encrypted_char] = chr(i)

# Decrypt the message
decrypted = ''.join(encryption_map.get(c, c) for c in encrypted)
print(f"Decrypted text: {decrypted}")
