"""MarketState."""
from dataclasses import dataclass
import numpy as np

@dataclass
class MarketState:
    symbol: str = "BTCUSDT"
    price: float = 0.0
    features: np.ndarray = None
    orderbook_imbalance: float = 0.0
    volatility: float = 0.0
    timestamp: int = 0

    def __post_init__(self):
        if self.features is None:
            self.features = np.zeros(32, dtype=np.float32)

    def to_vector(self) -> np.ndarray:
        return self.features
