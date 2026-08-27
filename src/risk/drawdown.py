"""Drawdown."""
import numpy as np

def max_drawdown(equity_curve: list[float]) -> float:
    peak = equity_curve[0]
    mdd = 0.0
    for v in equity_curve:
        if v > peak: peak = v
        dd = (peak - v)/peak if peak else 0
        mdd = max(mdd, dd)
    return mdd

def current_drawdown(equity_curve: list[float]) -> float:
    if not equity_curve: return 0.0
    peak = max(equity_curve)
    return (peak - equity_curve[-1])/peak if peak else 0.0

def drawdown_duration(equity_curve: list[float]) -> int:
    peak_idx = int(np.argmax(equity_curve))
    return len(equity_curve) - peak_idx - 1
