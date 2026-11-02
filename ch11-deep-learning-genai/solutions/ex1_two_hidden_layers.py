"""Exercise 11.1: two hidden layers of 64 neurons instead of one layer of 32."""
import torch
from torch import nn


def train(model: nn.Module, seed: int = 0) -> float:
    torch.manual_seed(seed)
    X = torch.randn(2000, 10)
    y = (X.sum(dim=1) > 0).float().unsqueeze(1)
    X_train, X_test, y_train, y_test = X[:1600], X[1600:], y[:1600], y[1600:]
    loss_fn = nn.BCEWithLogitsLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=1e-2)
    for _ in range(100):
        optimizer.zero_grad()
        loss_fn(model(X_train), y_train).backward()
        optimizer.step()
    with torch.no_grad():
        return ((torch.sigmoid(model(X_test)) > 0.5).float() == y_test).float().mean().item()


torch.manual_seed(1)
small = nn.Sequential(nn.Linear(10, 32), nn.ReLU(), nn.Linear(32, 1))
torch.manual_seed(1)
deeper = nn.Sequential(nn.Linear(10, 64), nn.ReLU(),
                       nn.Linear(64, 64), nn.ReLU(),
                       nn.Linear(64, 1))

acc_small, acc_deeper = train(small), train(deeper)
w_small = sum(p.numel() for p in small.parameters())
w_deeper = sum(p.numel() for p in deeper.parameters())
print(f"1 x 32 hidden:  test accuracy {acc_small:.3f}  ({w_small:,} weights)")
print(f"2 x 64 hidden:  test accuracy {acc_deeper:.3f}  ({w_deeper:,} weights)")

gain = acc_deeper - acc_small
if abs(gain) < 0.01:
    print(f"Practically the same accuracy with {w_deeper / w_small:.0f}x more weights.")
elif gain > 0:
    print(f"The deeper network gains {gain:.3f} accuracy for {w_deeper / w_small:.0f}x more weights.")
else:
    print(f"The deeper network is worse by {-gain:.3f}: extra capacity let it overfit the training set.")
print("The label is a simple sum of the inputs, almost a straight line, so extra layers have"
      " little to learn. Match the network's capacity to the difficulty of the pattern.")
