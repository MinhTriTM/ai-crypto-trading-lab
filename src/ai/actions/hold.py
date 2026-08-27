"""Hold."""
from dataclasses import dataclass
from .action import Action

@dataclass
class HoldAction(Action):
    symbol: str = "BTCUSDT"
    size_pct: float = 0.0
    leverage: float = 1.0

    def to_order(self, equity: float, price: float):
        return None

    def __str__(self):
        return "HOLD"
