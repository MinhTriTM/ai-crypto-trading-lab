"""HistoricalReplay - replay du lieu lich su theo dung thu tu thoi gian."""
import asyncio
from pathlib import Path
from typing import AsyncIterator, Optional
try:
    import pyarrow.parquet as pq
    _HAS_PYARROW = True
except ImportError:
    _HAS_PYARROW = False
    pq = None
from src.market.events.market_event import MarketEvent
from src.market.clock.market_clock import MarketClock

class HistoricalReplay:
    """Doc parquet/tick file va phat event theo timestamp, ton trong no-lookahead."""
    def __init__(self, data_path: str | Path, clock: MarketClock | None = None, speed: float = 1000.0):
        self.data_path = Path(data_path)
        self.clock = clock or MarketClock(speed=speed)
        self.speed = speed

    async def stream(self) -> AsyncIterator[MarketEvent]:
        files = sorted(self.data_path.rglob("*.parquet"))
        if _HAS_PYARROW:
            # neu co pyarrow, doc parquet
            if not files:
                import time, random
                ts = int(time.time()*1000)
                for i in range(100):
                    yield MarketEvent(symbol="BTCUSDT", timestamp=ts+i*100, payload={"p": 67000+i, "q": 0.01})
                    if self.speed < 100:
                        await asyncio.sleep(0.01)
                return
            for f in files:
                try:
                    table = pq.read_table(f)
                    df = table.to_pandas()
                except Exception:
                    continue
                df = df.sort_values("timestamp") if "timestamp" in df.columns else df
                for _, row in df.iterrows():
                    ev = MarketEvent(symbol=row.get("symbol","BTCUSDT"), timestamp=int(row.get("timestamp", 0)), payload=row.to_dict())
                    if self.clock.current_ms == 0:
                        self.clock.current_ms = ev.timestamp
                        self.clock.start_ms = ev.timestamp
                    else:
                        try:
                            self.clock.set(ev.timestamp)
                        except ValueError:
                            pass
                    yield ev
                    if self.speed < 500:
                        await asyncio.sleep(0.001)
        else:
            # fallback: tim csv neu khong co parquet, hoac sinh mock
            csv_files = sorted(self.data_path.rglob("*.csv"))
            if csv_files:
                import pandas as pd
                for f in csv_files:
                    try:
                        df = pd.read_csv(f)
                    except Exception:
                        continue
                    df = df.sort_values("timestamp") if "timestamp" in df.columns else df
                    for _, row in df.iterrows():
                        ev = MarketEvent(symbol=row.get("symbol","BTCUSDT"), timestamp=int(row.get("timestamp", 0)), payload=row.to_dict())
                        if self.clock.current_ms == 0:
                            self.clock.current_ms = ev.timestamp
                            self.clock.start_ms = ev.timestamp
                        else:
                            try:
                                self.clock.set(ev.timestamp)
                            except ValueError:
                                pass
                        yield ev
                        if self.speed < 500:
                            await asyncio.sleep(0.001)
                return
            # fallback mock
            import time, random
            ts = int(time.time()*1000)
            for i in range(100):
                yield MarketEvent(symbol="BTCUSDT", timestamp=ts+i*100, payload={"p": 67000+i, "q": 0.01})
                if self.speed < 100:
                    await asyncio.sleep(0.01)
            return

    def seek(self, timestamp_ms: int):
        self.clock.set(timestamp_ms)
