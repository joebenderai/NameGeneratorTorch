import torch
import torch.nn as nn
import torch.optim as optim

class RNN(nn.Module):
    def __init__(self, D_in, D_out, layers):
        super(RNN, self).__init__()
        self.lstm = nn.LSTM(D_in, D_out, layers)

    def forward(self, x):
        output, _ = self.lstm(x)
        return output

# hyper-parameters
D_in = 3
D_out = 4
layers = 3
lr = .5
seq_length = 2
batch_size = 64
C = D_out # number of categories for classifiction
epochs = 50000
print_every = 1000

model = RNN(D_in, D_out, layers)

x = torch.randn(seq_length, batch_size, D_in)
#y = torch.randn(seq_length, batch_size, D_out)
y = torch.empty(seq_length*batch_size*1, dtype=torch.long).random_(C)

criterion = nn.CrossEntropyLoss()
optimizer = optim.SGD(model.parameters(), lr=lr)
for t in range(epochs):
    y_pred = model(x)
    y_pred = y_pred.view(-1, D_out)

    loss = criterion(y_pred, y)
    if (t+1) % print_every == 0 or t == 0:
        print(t+1, loss.item())

    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
