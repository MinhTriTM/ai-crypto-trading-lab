"""MarketClock - dong ho thi truong."""
from dataclasses import dataclass

@dataclass
class MarketClock:
    current_ms: int = 0
    start_ms: int = 0
    speed: float = 1.0

    def now(self) -> int:
        return self.current_ms
    def advance(self, delta_ms: int):
        self.current_ms += int(delta_ms * self.speed)
    def set(self, ts_ms: int):
        if ts_ms < self.current_ms:
            raise ValueError(f"Khong the lui clock: {ts_ms} < {self.current_ms}")
        self.current_ms = ts_ms
    def elapsed_ms(self) -> int:
        return self.current_ms - self.start_ms
