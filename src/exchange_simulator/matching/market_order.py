"""MarketOrder helper."""
from dataclasses import dataclass

@dataclass
class MarketOrderSpec:
    symbol: str
    side: str  # buy | sell
    qty: float
    leverage: float = 1.0

    def to_order(self):
        from src.portfolio.order import Order
        import uuid
        return Order(id=str(uuid.uuid4()), symbol=self.symbol, side=self.side, type="market", qty=self.qty, leverage=self.leverage)
