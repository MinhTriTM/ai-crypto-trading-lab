"""Margin."""
from dataclasses import dataclass

@dataclass
class MarginAccount:
    balance: float = 1000.0
    used_margin: float = 0.0

    @property
    def free_margin(self) -> float:
        return self.balance - self.used_margin

    @property
    def margin_level(self) -> float:
        return self.balance / self.used_margin if self.used_margin else float('inf')

    def can_open(self, required: float) -> bool:
        return self.free_margin >= required
