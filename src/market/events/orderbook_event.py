"""OrderbookEvent - cap nhat so lenh."""
from dataclasses import dataclass, field
from typing import List, Tuple
from .market_event import MarketEvent

@dataclass
class OrderbookEvent(MarketEvent):
    bids: List[Tuple[float,float]] = field(default_factory=list)
    asks: List[Tuple[float,float]] = field(default_factory=list)
    first_update_id: int = 0
    final_update_id: int = 0
    is_snapshot: bool = False

    @classmethod
    def from_binance(cls, data: dict):
        bids = [(float(p), float(q)) for p,q in data.get('b', data.get('bids',[]))]
        asks = [(float(p), float(q)) for p,q in data.get('a', data.get('asks',[]))]
        return cls(
            source="binance",
            symbol=data.get('s','BTCUSDT'),
            event_type="orderbook",
            bids=bids, asks=asks,
            first_update_id=data.get('U',0),
            final_update_id=data.get('u',0),
            is_snapshot='lastUpdateId' in data,
            payload=data
        )
