"""Actor network."""
try:
    import torch
    import torch.nn as nn
    _TORCH = True
except ImportError:
    _TORCH = False
    torch = None
    nn = None

if _TORCH:
    class Actor(nn.Module):
        def __init__(self, state_dim: int = 48, action_dim: int = 3, hidden: int = 128):
            super().__init__()
            self.net = nn.Sequential(
                nn.Linear(state_dim, hidden),
                nn.ReLU(),
                nn.Linear(hidden, hidden),
                nn.ReLU(),
                nn.Linear(hidden, action_dim)
            )
        def forward(self, x):
            logits = self.net(x)
            return torch.softmax(logits, dim=-1)
        def act(self, state, deterministic: bool = False):
            import numpy as np
            self.eval()
            with torch.no_grad():
                s = torch.FloatTensor(state).unsqueeze(0)
                probs = self.forward(s).squeeze(0).numpy()
            if deterministic:
                return int(np.argmax(probs))
            return int(np.random.choice(len(probs), p=probs))
else:
    import numpy as np
    class Actor:
        def __init__(self, state_dim: int = 48, action_dim: int = 3, hidden: int = 128):
            self.state_dim = state_dim
            self.action_dim = action_dim
            self.W = np.random.randn(hidden, state_dim)*0.01
            self.W2 = np.random.randn(action_dim, hidden)*0.01
        def forward(self, x):
            h = np.tanh(self.W @ np.array(x))
            logits = self.W2 @ h
            e = np.exp(logits - np.max(logits))
            return e / e.sum()
        def act(self, state, deterministic: bool = False):
            probs = self.forward(np.array(state))
            if deterministic:
                return int(np.argmax(probs))
            return int(np.random.choice(len(probs), p=probs))
