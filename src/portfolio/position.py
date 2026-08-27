"""Position - vi the long/short."""
from dataclasses import dataclass

@dataclass
class Position:
    symbol: str
    side: str  # long | short | buy | sell
    qty: float
    entry_price: float
    mark_price: float = 0.0
    leverage: float = 1.0

    @property
    def notional(self) -> float:
        return self.qty * self.entry_price

    @property
    def is_long(self) -> bool:
        return self.side in ("long","buy")

    def unrealized_pnl(self, current_price: float) -> float:
        if self.is_long:
            return (current_price - self.entry_price) * self.qty
        else:
            return (self.entry_price - current_price) * self.qty

    def roe(self, current_price: float) -> float:
        margin = self.notional / self.leverage if self.leverage else self.notional
        pnl = self.unrealized_pnl(current_price)
        return pnl / margin if margin else 0.0

    def liquidation_price(self) -> float:
        # don gian
        move = self.entry_price / self.leverage * 0.9
        return self.entry_price - move if self.is_long else self.entry_price + move
