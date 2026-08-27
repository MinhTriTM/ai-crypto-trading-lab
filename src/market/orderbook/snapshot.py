"""Snapshot - anh chup orderbook tai 1 thoi diem."""
from dataclasses import dataclass, field
from typing import List, Tuple
import time

@dataclass
class Snapshot:
    symbol: str
    bids: List[Tuple[float,float]]
    asks: List[Tuple[float,float]]
    timestamp: int = field(default_factory=lambda: int(time.time()*1000))
    last_update_id: int = 0

    def to_orderbook(self):
        from .orderbook import OrderBook
        ob = OrderBook(symbol=self.symbol)
        ob.apply_snapshot(self.bids, self.asks, self.last_update_id)
        ob.timestamp = self.timestamp
        return ob
