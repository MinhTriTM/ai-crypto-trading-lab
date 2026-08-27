"""Slippage model."""
from dataclasses import dataclass

@dataclass
class SlippageModel:
    base_bps: float = 5.0
    volume_impact: float = 0.0001

    def calculate(self, qty: float, price: float, book_depth_qty: float = 10.0) -> float:
        # slippage tang theo qty / depth
        impact = (qty / max(book_depth_qty, 0.001)) * self.volume_impact
        return price * (self.base_bps/10000 + impact)

    def apply(self, price: float, side: str, slippage: float) -> float:
        return price + slippage if side=="buy" else price - slippage
