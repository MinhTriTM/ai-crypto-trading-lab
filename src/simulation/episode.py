"""Episode - mot cuoc doi giao dich."""
from dataclasses import dataclass, field
from typing import List
import time

@dataclass
class Episode:
    id: str = field(default_factory=lambda: str(int(time.time()*1000)))
    steps: List[dict] = field(default_factory=list)
    start_equity: float = 1000.0
    end_equity: float = 1000.0
    max_equity: float = 1000.0
    min_equity: float = 1000.0
    trades: int = 0
    done_reason: str = "truncated"

    def add_step(self, obs, action, reward, equity):
        self.steps.append({"obs": obs, "action": str(action), "reward": reward, "equity": equity})
        self.end_equity = equity
        self.max_equity = max(self.max_equity, equity)
        self.min_equity = min(self.min_equity, equity)

    @property
    def return_pct(self) -> float:
        return (self.end_equity - self.start_equity)/self.start_equity if self.start_equity else 0

    @property
    def length(self) -> int:
        return len(self.steps)

    def to_dict(self):
        return {"id": self.id, "steps": self.length, "start": self.start_equity, "end": self.end_equity, "return": self.return_pct, "reason": self.done_reason}
