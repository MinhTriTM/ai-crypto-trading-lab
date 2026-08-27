"""Sampler."""
import random
import numpy as np

class Sampler:
    def __init__(self, strategy: str = "uniform"):
        self.strategy = strategy

    def sample(self, buffer, batch_size: int):
        if self.strategy == "uniform":
            return buffer.sample(batch_size)
        elif self.strategy == "prioritized":
            # placeholder: lay theo reward cao
            exps = list(buffer.buffer)
            exps.sort(key=lambda e: abs(e.reward), reverse=True)
            return exps[:batch_size]
        return buffer.sample(batch_size)
