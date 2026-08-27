"""Probability."""
import numpy as np

def prob_up(returns: list[float]) -> float:
    arr = np.array(returns)
    return float((arr > 0).mean()) if len(arr) else 0.5

def prob_target_hit(returns: list[float], target: float = 0.01) -> float:
    arr = np.array(returns)
    return float((arr >= target).mean()) if len(arr) else 0.0

def expected_value(returns: list[float]) -> float:
    return float(np.mean(returns)) if returns else 0.0
