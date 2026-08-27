"""TD3."""
from dataclasses import dataclass

@dataclass
class TD3Config:
    lr: float = 3e-4
    gamma: float = 0.99
    tau: float = 0.005
    policy_noise: float = 0.2
    noise_clip: float = 0.5
    policy_freq: int = 2

class TD3:
    def __init__(self, actor, critic, config: TD3Config = TD3Config()):
        self.actor = actor
        self.critic = critic
        self.cfg = config

    def update(self, batch):
        return {"loss": 0.0}
