"""OrderBook - so lenh realtime."""
from dataclasses import dataclass, field
from typing import Dict

@dataclass
class OrderBook:
    symbol: str
    bids: Dict[float,float] = field(default_factory=dict)
    asks: Dict[float,float] = field(default_factory=dict)
    last_update_id: int = 0
    timestamp: int = 0

    def apply_snapshot(self, bids, asks, update_id: int):
        self.bids = {float(p): float(q) for p,q in bids}
        self.asks = {float(p): float(q) for p,q in asks}
        self.last_update_id = update_id

    def apply_delta(self, bids, asks, update_id: int):
        for p,q in bids:
            pf, qf = float(p), float(q)
            if qf == 0: self.bids.pop(pf, None)
            else: self.bids[pf] = qf
        for p,q in asks:
            pf, qf = float(p), float(q)
            if qf == 0: self.asks.pop(pf, None)
            else: self.asks[pf] = qf
        self.last_update_id = update_id

    @property
    def best_bid(self) -> float:
        return max(self.bids) if self.bids else 0.0
    @property
    def best_ask(self) -> float:
        return min(self.asks) if self.asks else 0.0
    @property
    def spread(self) -> float:
        return self.best_ask - self.best_bid if self.best_bid and self.best_ask else 0.0
    @property
    def mid_price(self) -> float:
        return (self.best_bid + self.best_ask)/2 if self.best_bid and self.best_ask else 0.0
    @property
    def spread_bps(self) -> float:
        mid = self.mid_price
        return (self.spread / mid * 10000) if mid else 0.0

    def depth(self, levels: int = 5):
        sb = sorted(self.bids.items(), reverse=True)[:levels]
        sa = sorted(self.asks.items())[:levels]
        return sb, sa

    def to_dict(self):
        return {"symbol": self.symbol, "best_bid": self.best_bid, "best_ask": self.best_ask, "spread": self.spread, "mid": self.mid_price}
