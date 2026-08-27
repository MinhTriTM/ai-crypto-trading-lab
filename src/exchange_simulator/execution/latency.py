"""Latency model."""
import random
from dataclasses import dataclass

@dataclass
class LatencyModel:
    mean_ms: float = 8.1
    jitter_ms: float = 2.0
    p99_ms: float = 20.0

    def sample(self) -> float:
        # log-normal approx
        return max(0.1, random.gauss(self.mean_ms, self.jitter_ms))

    def delayed_timestamp(self, decision_ts: int) -> int:
        return int(decision_ts + self.sample())
