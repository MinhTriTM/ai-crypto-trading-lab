"""Trade - giao dich da khop."""
from dataclasses import dataclass, field
import uuid, time

@dataclass
class Trade:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    order_id: str = ""
    symbol: str = "BTCUSDT"
    side: str = "buy"
    price: float = 0.0
    qty: float = 0.0
    timestamp: int = field(default_factory=lambda: int(time.time()*1000))
    fee: float = 0.0
    pnl: float = 0.0
