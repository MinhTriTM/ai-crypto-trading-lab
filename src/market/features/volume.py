"""Volume features."""
import numpy as np

def volume_imbalance(buy_vol: float, sell_vol: float) -> float:
    tot = buy_vol + sell_vol
    return (buy_vol - sell_vol)/tot if tot else 0.0

def vwap(prices: np.ndarray, volumes: np.ndarray) -> float:
    return float(np.sum(prices*volumes)/np.sum(volumes)) if np.sum(volumes) else 0.0
