"""Action base."""
from abc import ABC, abstractmethod
from dataclasses import dataclass

@dataclass
class Action(ABC):
    symbol: str = "BTCUSDT"
    size_pct: float = 0.0
    leverage: float = 1.0

    @abstractmethod
    def to_order(self, equity: float, price: float):
        pass

    @property
    def is_hold(self) -> bool:
        return self.size_pct == 0
