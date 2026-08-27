"""Orderflow features."""
import numpy as np

def cumulative_volume_delta(trades: list) -> float:
    cvd = 0.0
    for t in trades:
        sign = 1 if t.get('side')=='buy' else -1
        cvd += sign * t.get('qty',0)
    return cvd

def trade_intensity(trades: list, window_ms: int = 1000) -> float:
    if not trades: return 0.0
    now = trades[-1].get('timestamp',0)
    recent = [t for t in trades if now - t.get('timestamp',0) <= window_ms]
    return len(recent) / (window_ms/1000)
