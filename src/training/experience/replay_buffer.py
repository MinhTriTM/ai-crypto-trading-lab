"""ReplayBuffer."""
import random
from collections import deque
import numpy as np
from .experience import Experience

class ReplayBuffer:
    def __init__(self, capacity: int = 1_000_000):
        self.buffer = deque(maxlen=capacity)

    def add(self, exp: Experience):
        self.buffer.append(exp)

    def sample(self, batch_size: int) -> list[Experience]:
        return random.sample(self.buffer, min(batch_size, len(self.buffer)))

    def __len__(self):
        return len(self.buffer)

    def to_batch(self, exps: list[Experience]) -> dict:
        return {
            "states": np.stack([e.state for e in exps]),
            "actions": np.array([e.action for e in exps]),
            "rewards": np.array([e.reward for e in exps]),
            "next_states": np.stack([e.next_state for e in exps]),
            "dones": np.array([e.done for e in exps])
        }
