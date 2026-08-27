"""Policy - anh xa state -> distribution over actions."""
import numpy as np
from dataclasses import dataclass

@dataclass
class PolicyConfig:
    state_dim: int = 32
    action_dim: int = 3
    hidden_dim: int = 128

class Policy:
    def __init__(self, config: PolicyConfig = PolicyConfig()):
        self.cfg = config
        # placeholder linear policy
        self.W = np.random.randn(config.hidden_dim, config.state_dim) * 0.01
        self.W2 = np.random.randn(config.action_dim, config.hidden_dim) * 0.01

    def forward(self, state: np.ndarray) -> np.ndarray:
        h = np.tanh(self.W @ state)
        logits = self.W2 @ h
        # softmax
        e = np.exp(logits - np.max(logits))
        return e / e.sum()

    def predict(self, state: np.ndarray) -> int:
        probs = self.forward(state)
        return int(np.argmax(probs))

    def sample(self, state: np.ndarray) -> int:
        probs = self.forward(state)
        return int(np.random.choice(len(probs), p=probs))
