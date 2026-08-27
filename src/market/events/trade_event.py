"""TradeEvent - tick giao dich that."""
from dataclasses import dataclass
from .market_event import MarketEvent

@dataclass
class TradeEvent(MarketEvent):
    price: float = 0.0
    qty: float = 0.0
    side: str = "buy"
    is_buyer_maker: bool = False

    @classmethod
    def from_binance(cls, data: dict):
        return cls(
            source="binance",
            symbol=data.get('s','BTCUSDT'),
            event_type="trade",
            timestamp=data.get('T', data.get('E',0)),
            price=float(data.get('p',0)),
            qty=float(data.get('q',0)),
            side="sell" if data.get('m') else "buy",
            is_buyer_maker=bool(data.get('m', False)),
            payload=data
        )
