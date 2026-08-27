"""Scenario - kich ban thi truong."""
from dataclasses import dataclass
from enum import Enum

class ScenarioType(str, Enum):
    BULL = "bull"
    BEAR = "bear"
    SIDEWAYS = "sideways"
    FLASH_CRASH = "flash_crash"
    VOLATILITY_SPIKE = "volatility_spike"

@dataclass
class Scenario:
    type: ScenarioType = ScenarioType.SIDEWAYS
    symbol: str = "BTCUSDT"
    duration_ms: int = 3600000  # 1h
    volatility: float = 0.01
    trend: float = 0.0  # drift per step
    description: str = ""

    def generate_prices(self, start: float = 67000, steps: int = 1000) -> list[float]:
        import random
        prices = [start]
        for _ in range(steps-1):
            if self.type == ScenarioType.FLASH_CRASH and len(prices) == steps//2:
                # dot ngot giam 10%
                prices.append(prices[-1] * 0.9)
            else:
                change = random.gauss(self.trend, self.volatility) * prices[-1] * 0.001
                prices.append(max(1000, prices[-1] + change))
        return prices
