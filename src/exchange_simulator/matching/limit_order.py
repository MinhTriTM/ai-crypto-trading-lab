"""LimitOrder helper."""
from dataclasses import dataclass

@dataclass
class LimitOrderSpec:
    symbol: str
    side: str
    qty: float
    price: float
    leverage: float = 1.0

    def to_order(self):
        from src.portfolio.order import Order
        import uuid
        return Order(id=str(uuid.uuid4()), symbol=self.symbol, side=self.side, type="limit", qty=self.qty, price=self.price, leverage=self.leverage)
