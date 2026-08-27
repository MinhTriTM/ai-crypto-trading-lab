"""LatencyClock - mo phong do tre."""
import random
from dataclasses import dataclass

@dataclass
class LatencyClock:
    data_latency_ms: float = 4.3
    order_latency_ms: float = 8.1
    jitter_ms: float = 2.0

    def data_arrival_time(self, event_ts: int) -> int:
        jitter = random.uniform(-self.jitter_ms, self.jitter_ms)
        return int(event_ts + self.data_latency_ms + jitter)
    def order_arrival_time(self, decision_ts: int) -> int:
        jitter = random.uniform(-self.jitter_ms, self.jitter_ms)
        return int(decision_ts + self.order_latency_ms + jitter)
    def is_visible(self, event_ts: int, now_ms: int) -> bool:
        return self.data_arrival_time(event_ts) <= now_ms
