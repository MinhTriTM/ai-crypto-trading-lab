"""ReplayClock - dong ho tua nhanh cho backtest."""
from src.market.clock.market_clock import MarketClock

class ReplayClock(MarketClock):
    """Cho phep tua nhanh va jump."""
    def __init__(self, start_ms: int = 0, speed: float = 1000.0):
        super().__init__(current_ms=start_ms, start_ms=start_ms, speed=speed)

    def jump(self, target_ms: int):
        # Chi tien
        self.set(target_ms)

    def fast_forward(self, delta_ms: int):
        self.advance(delta_ms)
