"""EventReplay - phat lai event tu buffer/memory."""
from collections import deque
from typing import List
from src.market.events.market_event import MarketEvent

class EventReplay:
    def __init__(self, events: List[MarketEvent]):
        self.events = sorted(events, key=lambda e: e.timestamp)
        self.idx = 0

    def next(self) -> MarketEvent | None:
        if self.idx >= len(self.events):
            return None
        ev = self.events[self.idx]
        self.idx += 1
        return ev

    def peek(self, n: int = 1) -> List[MarketEvent]:
        return self.events[self.idx:self.idx+n]

    def reset(self):
        self.idx = 0

    def slice(self, start_ms: int, end_ms: int) -> List[MarketEvent]:
        return [e for e in self.events if start_ms <= e.timestamp <= end_ms]
