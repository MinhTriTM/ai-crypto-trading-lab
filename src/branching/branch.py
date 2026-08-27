"""Branch - mot nhanh giao dich."""
from dataclasses import dataclass, field
import uuid
from typing import Optional

@dataclass
class Branch:
    id: str = field(default_factory=lambda: uuid.uuid4().hex[:6].upper())
    parent_id: Optional[str] = None
    symbol: str = "BTCUSDT"
    action: str = "HOLD"  # HOLD | LONG | SHORT
    capital: float = 1000.0
    position_pct: float = 0.0
    leverage: float = 1.0
    decision_offset_ms: int = 0
    data_latency_ms: float = 4.3
    order_latency_ms: float = 8.1
    target: float = 10000.0
    depth: int = 0  # do sau trong cay
    pnl: float = 0.0
    status: str = "active"  # active | closed | pruned

    def to_dict(self):
        return {"id": self.id, "parent": self.parent_id, "symbol": self.symbol, "action": self.action, "capital": self.capital, "pos": self.position_pct, "lev": self.leverage, "target": self.target, "depth": self.depth}

    def is_leaf(self) -> bool:
        return self.status == "active"
