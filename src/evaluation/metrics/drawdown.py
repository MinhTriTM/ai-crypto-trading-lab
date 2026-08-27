"""Drawdown metrics."""
import numpy as np

def max_drawdown(equities: list[float]) -> float:
    peak = equities[0] if equities else 1
    mdd = 0.0
    for v in equities:
        if v > peak: peak = v
        dd = (peak - v)/peak if peak else 0
        mdd = max(mdd, dd)
    return mdd

def avg_drawdown(equities: list[float]) -> float:
    peak = equities[0] if equities else 1
    dds = []
    for v in equities:
        if v > peak: peak = v
        dds.append((peak-v)/peak if peak else 0)
    return float(np.mean(dds)) if dds else 0

def drawdown_duration(equities: list[float]) -> int:
    peak_idx = int(np.argmax(equities)) if equities else 0
    return len(equities) - peak_idx - 1
