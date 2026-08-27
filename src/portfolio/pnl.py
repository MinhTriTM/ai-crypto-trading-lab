"""PnL."""
from dataclasses import dataclass

@dataclass
class PnL:
    realized: float = 0.0
    unrealized: float = 0.0
    fees: float = 0.0
    funding: float = 0.0

    @property
    def total(self) -> float:
        return self.realized + self.unrealized - self.fees + self.funding

    @property
    def net_profit(self) -> float:
        return self.realized - self.fees

    def update_unrealized(self, value: float):
        self.unrealized = value
