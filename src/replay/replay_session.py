"""ReplaySession - phien replay hoan chinh voi start/end va callback."""
from dataclasses import dataclass
from typing import Callable, Optional
from .historical_replay import HistoricalReplay
from .replay_clock import ReplayClock
from src.market.events.market_event import MarketEvent

@dataclass
class ReplaySession:
    data_path: str
    start_ms: int | None = None
    end_ms: int | None = None
    speed: float = 1000.0
    on_event: Optional[Callable[[MarketEvent], None]] = None

    async def run(self):
        clock = ReplayClock(start_ms=self.start_ms or 0, speed=self.speed)
        replay = HistoricalReplay(self.data_path, clock=clock, speed=self.speed)
        async for ev in replay.stream():
            if self.start_ms and ev.timestamp < self.start_ms:
                continue
            if self.end_ms and ev.timestamp > self.end_ms:
                break
            if self.on_event:
                self.on_event(ev)
            yield ev
