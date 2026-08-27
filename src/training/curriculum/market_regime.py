"""MarketRegime."""
from enum import Enum

class MarketRegime(str, Enum):
    BULL = "bull"
    BEAR = "bear"
    SIDEWAYS = "sideways"
    VOLATILE = "volatile"
    FLASH_CRASH = "flash_crash"
    MIXED = "mixed"

def detect_regime(returns: list[float]) -> MarketRegime:
    import numpy as np
    arr = np.array(returns)
    mean = np.mean(arr)
    std = np.std(arr)
    if std > 0.02:
        return MarketRegime.VOLATILE
    if mean > 0.001:
        return MarketRegime.BULL
    if mean < -0.001:
        return MarketRegime.BEAR
    return MarketRegime.SIDEWAYS
