"""Critic network."""
try:
    import torch
    import torch.nn as nn
    _TORCH = True
except ImportError:
    _TORCH = False
    torch = None
    nn = None

if _TORCH:
    class Critic(nn.Module):
        def __init__(self, state_dim: int = 48, hidden: int = 128):
            super().__init__()
            self.net = nn.Sequential(
                nn.Linear(state_dim, hidden),
                nn.ReLU(),
                nn.Linear(hidden, hidden),
                nn.ReLU(),
                nn.Linear(hidden, 1)
            )
        def forward(self, x):
            return self.net(x).squeeze(-1)
else:
    import numpy as np
    class Critic:
        def __init__(self, state_dim: int = 48, hidden: int = 128):
            self.W = np.random.randn(hidden, state_dim)*0.01
            self.W2 = np.random.randn(1, hidden)*0.01
        def forward(self, x):
            h = np.tanh(self.W @ np.array(x))
            return float(self.W2 @ h)
