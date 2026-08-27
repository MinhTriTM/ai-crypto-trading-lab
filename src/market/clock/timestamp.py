"""Timestamp utils."""
import time
from datetime import datetime, timezone

def now_ms() -> int:
    return int(time.time()*1000)
def to_iso(ms: int) -> str:
    return datetime.fromtimestamp(ms/1000, tz=timezone.utc).isoformat()
def from_iso(s: str) -> int:
    return int(datetime.fromisoformat(s).timestamp()*1000)
def floor_ms(ts: int, interval: int) -> int:
    return ts // interval * interval
