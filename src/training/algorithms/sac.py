"""SAC."""
from dataclasses import dataclass
try:
    import torch
    import torch.nn as nn
    import torch.optim as optim
    _TORCH = True
except ImportError:
    _TORCH = False
    torch = None

@dataclass
class SACConfig:
    lr: float = 3e-4
    gamma: float = 0.99
    tau: float = 0.005
    buffer_size: int = 1_000_000
    batch_size: int = 256

class SAC:
    def __init__(self, actor, critic, config: SACConfig = SACConfig()):
        self.actor = actor
        self.critic = critic
        self.cfg = config
        if _TORCH:
            self.optimizer = optim.Adam(list(actor.parameters())+list(critic.parameters()), lr=config.lr)
            self.target_critic = type(critic)(48) if hasattr(critic, 'net') else critic
        else:
            self.optimizer = None
            self.target_critic = critic
    def update(self, batch):
        return {"loss": 0.0}
    def select_action(self, state, deterministic=False):
        return self.actor.act(state, deterministic)
