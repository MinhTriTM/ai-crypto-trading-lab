"""MarketEvent - su kien thi truong co so."""
from dataclasses import dataclass, field
from typing import Any
import time, uuid

@dataclass
class MarketEvent:
    event_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    source: str = "unknown"
    symbol: str = "BTCUSDT"
    event_type: str = "trade"
    timestamp: int = field(default_factory=lambda: int(time.time()*1000))
    recv_timestamp: int = field(default_factory=lambda: int(time.time()*1000))
    payload: dict = field(default_factory=dict)

    @classmethod
    def from_raw(cls, raw: dict, source: str = "unknown"):
        return cls(source=source, payload=raw, symbol=raw.get('s', raw.get('symbol','BTCUSDT')))

    @property
    def latency_ms(self) -> int:
        return self.recv_timestamp - self.timestamp
