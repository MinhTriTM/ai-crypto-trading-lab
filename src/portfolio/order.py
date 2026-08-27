"""Order."""
from dataclasses import dataclass, field
import uuid

@dataclass
class Order:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    symbol: str = "BTCUSDT"
    side: str = "buy"  # buy | sell
    type: str = "market"  # market | limit
    qty: float = 0.01
    price: float = 0.0  # for limit
    leverage: float = 1.0
    status: str = "pending"  # pending | open | filled | partially_filled | cancelled
    filled_qty: float = 0.0
    timestamp: int = 0
