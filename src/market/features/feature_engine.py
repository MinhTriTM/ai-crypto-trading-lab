"""FeatureEngine - tong hop moi feature thanh vector cho AI."""
import numpy as np
from dataclasses import dataclass
from src.market.orderbook.orderbook import OrderBook
from . import price, volume, volatility, imbalance

@dataclass
class FeatureConfig:
    lookback: int = 100
    levels: int = 5
    with_orderbook: bool = True

class FeatureEngine:
    def __init__(self, config: FeatureConfig = FeatureConfig()):
        self.cfg = config
        self._prices: list[float] = []
        self._volumes: list[float] = []
        self._ob: OrderBook | None = None

    def update(self, price_val: float, volume_val: float, ob: OrderBook | None = None):
        self._prices.append(price_val)
        self._volumes.append(volume_val)
        if len(self._prices) > self.cfg.lookback:
            self._prices.pop(0); self._volumes.pop(0)
        self._ob = ob

    def build(self) -> np.ndarray:
        if len(self._prices) < 2:
            return np.zeros(32, dtype=np.float32)
        p = np.array(self._prices, dtype=np.float64)
        v = np.array(self._volumes, dtype=np.float64)
        feats = []
        rets = price.log_returns(p)
        feats += [float(np.mean(rets[-10:])), float(np.std(rets[-10:])), price.moving_average(p,5), price.moving_average(p,20)]
        feats += [volatility.realized_volatility(rets,20)]
        feats += [volume.vwap(p,v), float(np.mean(v[-10:]))]
        if self.cfg.with_orderbook and self._ob:
            feats += [imbalance.book_imbalance(self._ob,5), self._ob.spread_bps, imbalance.weighted_mid_price(self._ob)]
        else:
            feats += [0.0,0.0,0.0]
        arr = np.array(feats, dtype=np.float32)
        if len(arr) < 32:
            arr = np.pad(arr, (0, 32-len(arr)))
        else:
            arr = arr[:32]
        return arr
