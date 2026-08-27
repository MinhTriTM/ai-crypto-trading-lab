"""Decision - ket qua quyet dinh cua AI."""
from dataclasses import dataclass
from ..actions.action import Action
import time

@dataclass
class Decision:
    action: Action
    confidence: float = 0.5
    timestamp: int = 0
    latency_ms: float = 0.0
    reasoning: str = ""

    def __post_init__(self):
        if self.timestamp == 0:
            self.timestamp = int(time.time()*1000)

    def to_dict(self):
        return {"action": str(self.action), "confidence": self.confidence, "timestamp": self.timestamp, "reasoning": self.reasoning}
