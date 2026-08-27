"""Time utils."""
import time
from datetime import datetime, timezone

def now_ms() -> int:
    return int(time.time()*1000)

def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()

def ms_to_iso(ms: int) -> str:
    return datetime.fromtimestamp(ms/1000, tz=timezone.utc).isoformat()

def iso_to_ms(s: str) -> int:
    return int(datetime.fromisoformat(s).timestamp()*1000)

def sleep_ms(ms: int):
    time.sleep(ms/1000)
