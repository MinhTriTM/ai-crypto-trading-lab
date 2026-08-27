"""LiquidationEvent - thanh ly futures."""
from dataclasses import dataclass
from .market_event import MarketEvent

@dataclass
class LiquidationEvent(MarketEvent):
    side: str = "buy"
    price: float = 0.0
    qty: float = 0.0

    @classmethod
    def from_binance(cls, data: dict):
        o = data.get('o', data)
        return cls(
            source="binance",
            symbol=o.get('s','BTCUSDT'),
            event_type="liquidation",
            side=o.get('S','BUY').lower(),
            price=float(o.get('p',0)),
            qty=float(o.get('q',0)),
            payload=data
        )
