"""Latency dimension."""
import random
from dataclasses import dataclass

@dataclass
class LatencyDimension:
    data_latencies: list[float] = None
    order_latencies: list[float] = None
    def __post_init__(self):
        if self.data_latencies is None:
            self.data_latencies = [1.0, 4.3, 10.0, 20.0]
        if self.order_latencies is None:
            self.order_latencies = [5.0, 8.1, 15.0, 30.0]
    def sample_data(self) -> float:
        return random.choice(self.data_latencies)
    def sample_order(self) -> float:
        return random.choice(self.order_latencies)
