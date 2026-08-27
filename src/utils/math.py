"""Math utils."""
import numpy as np

def sigmoid(x: float) -> float:
    return 1 / (1 + np.exp(-x))

def softmax(logits: np.ndarray) -> np.ndarray:
    e = np.exp(logits - np.max(logits))
    return e / e.sum()

def normalize(x: np.ndarray) -> np.ndarray:
    n = np.linalg.norm(x)
    return x / n if n else x

def ema_update(prev: float, new: float, alpha: float = 0.1) -> float:
    return alpha * new + (1-alpha) * prev

def clamp(x: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, x))
