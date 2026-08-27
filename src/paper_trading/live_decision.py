"""LiveDecision - quyet dinh realtime co latency."""
from dataclasses import dataclass
import time
from src.ai.agent.decision import Decision
from src.ai.actions.action import Action

@dataclass
class LiveDecision(Decision):
    received_at: int = 0
    executed_at: int = 0

    def latency(self) -> float:
        return (self.executed_at - self.received_at) if self.received_at and self.executed_at else 0

    @classmethod
    def from_action(cls, action: Action, confidence: float = 0.5):
        now = int(time.time()*1000)
        return cls(action=action, confidence=confidence, timestamp=now, received_at=now)
