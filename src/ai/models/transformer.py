"""Transformer cho market sequence."""
try:
    import torch
    import torch.nn as nn
    _TORCH = True
except ImportError:
    _TORCH = False
    torch = None
    nn = None

if _TORCH:
    class MarketTransformer(nn.Module):
        """Bien doi chuoi market features thanh embedding."""
        def __init__(self, input_dim: int = 32, d_model: int = 64, nhead: int = 4, num_layers: int = 2):
            super().__init__()
            self.input_proj = nn.Linear(input_dim, d_model)
            encoder_layer = nn.TransformerEncoderLayer(d_model=d_model, nhead=nhead, batch_first=True)
            self.transformer = nn.TransformerEncoder(encoder_layer, num_layers=num_layers)
            self.out = nn.Linear(d_model, d_model)
        def forward(self, x):
            h = self.input_proj(x)
            h = self.transformer(h)
            return self.out(h[:, -1, :])
else:
    import numpy as np
    class MarketTransformer:
        def __init__(self, input_dim: int = 32, d_model: int = 64, nhead: int = 4, num_layers: int = 2):
            self.input_dim = input_dim
            self.d_model = d_model
        def forward(self, x):
            return np.random.randn(x.shape[0], self.d_model).astype(np.float32)
