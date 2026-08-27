"""Short."""
from dataclasses import dataclass
from .action import Action
from src.portfolio.order import Order
import uuid

@dataclass
class ShortAction(Action):
    symbol: str = "BTCUSDT"
    size_pct: float = 0.1
    leverage: float = 2.0

    def to_order(self, equity: float, price: float):
        qty = (equity * self.size_pct * self.leverage) / price if price else 0
        return Order(id=str(uuid.uuid4()), symbol=self.symbol, side="sell", type="market", qty=qty, leverage=self.leverage)

    def __str__(self):
        return f"SHORT {self.symbol} {self.size_pct:.1%} x{self.leverage}"
