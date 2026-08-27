"""Sharpe."""
import numpy as np

def sharpe_ratio(returns: list[float], risk_free: float = 0.0, periods_per_year: int = 365*24*60) -> float:
    if not returns or len(returns) < 2:
        return 0.0
    arr = np.array(returns)
    excess = arr - risk_free/periods_per_year
    std = np.std(excess)
    if std == 0:
        return 0.0
    return float(np.mean(excess) / std * np.sqrt(periods_per_year))

def sortino_ratio(returns: list[float], risk_free: float = 0.0) -> float:
    if not returns: return 0.0
    arr = np.array(returns)
    downside = arr[arr < 0]
    if len(downside) == 0:
        return float(np.mean(arr) * 100)
    return float(np.mean(arr) / np.std(downside) * np.sqrt(365*24*60))
