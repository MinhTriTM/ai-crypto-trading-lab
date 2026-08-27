"""PositionTarget - dat muc tieu vi the cu the."""
from dataclasses import dataclass
from .action import Action
from src.portfolio.order import Order
import uuid

@dataclass
class PositionTargetAction(Action):
    symbol: str = "BTCUSDT"
    target_pct: float = 0.2  # muc tieu % equity
    leverage: float = 2.0
    current_pct: float = 0.0

    @property
    def delta_pct(self) -> float:
        return self.target_pct - self.current_pct

    def to_order(self, equity: float, price: float):
        if abs(self.delta_pct) < 0.01:
            return None
        side = "buy" if self.delta_pct > 0 else "sell"
        qty = abs(equity * self.delta_pct * self.leverage) / price if price else 0
        return Order(id=str(uuid.uuid4()), symbol=self.symbol, side=side, type="market", qty=qty, leverage=self.leverage)

    def __str__(self):
        return f"TARGET {self.symbol} {self.current_pct:.1%} -> {self.target_pct:.1%}"
