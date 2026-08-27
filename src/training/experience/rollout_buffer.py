"""RolloutBuffer cho PPO."""
import numpy as np
from collections import deque

class RolloutBuffer:
    def __init__(self, size: int = 2048, state_dim: int = 48):
        self.size = size
        self.state_dim = state_dim
        self.reset()

    def reset(self):
        self.states = []
        self.actions = []
        self.rewards = []
        self.values = []
        self.log_probs = []
        self.dones = []

    def add(self, state, action, reward, value, log_prob, done):
        self.states.append(state)
        self.actions.append(action)
        self.rewards.append(reward)
        self.values.append(value)
        self.log_probs.append(log_prob)
        self.dones.append(done)

    def compute_returns(self, gamma: float = 0.99, gae_lambda: float = 0.95):
        returns = []
        gae = 0
        for i in reversed(range(len(self.rewards))):
            delta = self.rewards[i] + gamma * (self.values[i+1] if i+1 < len(self.values) else 0) * (1-self.dones[i]) - self.values[i]
            gae = delta + gamma * gae_lambda * (1-self.dones[i]) * gae
            returns.insert(0, gae + self.values[i])
        self.returns = returns

    def get(self):
        return {
            "states": np.array(self.states),
            "actions": np.array(self.actions),
            "rewards": np.array(self.rewards),
            "returns": np.array(getattr(self, 'returns', self.rewards)),
            "values": np.array(self.values)
        }

    def __len__(self):
        return len(self.states)
