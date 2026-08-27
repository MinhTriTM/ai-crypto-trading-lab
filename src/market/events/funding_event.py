"""FundingEvent - funding rate cho futures."""
from dataclasses import dataclass
from .market_event import MarketEvent

@dataclass
class FundingEvent(MarketEvent):
    funding_rate: float = 0.0
    mark_price: float = 0.0
    next_funding_time: int = 0

    @classmethod
    def from_binance(cls, data: dict):
        return cls(
            source="binance",
            symbol=data.get('s','BTCUSDT'),
            event_type="funding",
            funding_rate=float(data.get('r',0)),
            mark_price=float(data.get('p',0)),
            payload=data
        )
