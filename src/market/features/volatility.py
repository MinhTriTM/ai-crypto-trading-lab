"""Volatility features."""
import numpy as np

def realized_volatility(returns: np.ndarray, window: int = 60) -> float:
    return float(np.std(returns[-window:]) * np.sqrt(60*24*365))

def parkinson_vol(high: np.ndarray, low: np.ndarray) -> float:
    return float(np.sqrt(np.mean(np.log(high/low)**2) / (4*np.log(2))))
