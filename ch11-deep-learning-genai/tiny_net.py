"""Chapter 11.3: a small neural network in PyTorch, trained with gradient descent."""
import torch
from torch import nn

torch.manual_seed(0)

# Toy data: 10 input features, label is 1 when their sum is positive
X = torch.randn(2000, 10)
y = (X.sum(dim=1) > 0).float().unsqueeze(1)
X_train, X_test, y_train, y_test = X[:1600], X[1600:], y[:1600], y[1600:]

model = nn.Sequential(
    nn.Linear(10, 32),
    nn.ReLU(),
    nn.Linear(32, 1),          # outputs a raw score (a "logit")
)
loss_fn = nn.BCEWithLogitsLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=1e-2)

for epoch in range(100):
    optimizer.zero_grad()                       # reset gradients from the last step
    loss = loss_fn(model(X_train), y_train)     # forward pass + loss
    loss.backward()                             # backpropagation
    optimizer.step()                            # update weights
    if epoch % 20 == 0:
        print(f"epoch {epoch:3d}  loss {loss.item():.4f}")

with torch.no_grad():
    predictions = (torch.sigmoid(model(X_test)) > 0.5).float()
    accuracy = (predictions == y_test).float().mean().item()
print(f"test accuracy: {accuracy:.3f}")
