"""Price features."""
import numpy as np

def returns(prices: np.ndarray) -> np.ndarray:
    return np.diff(prices) / prices[:-1]

def log_returns(prices: np.ndarray) -> np.ndarray:
    return np.diff(np.log(prices))

def moving_average(prices: np.ndarray, window: int) -> float:
    return float(np.mean(prices[-window:]))

def ema(prices: np.ndarray, span: int) -> float:
    alpha = 2/(span+1)
    ema_val = prices[0]
    for p in prices[1:]:
        ema_val = alpha*p + (1-alpha)*ema_val
    return float(ema_val)
