"""Risk penalty."""
def risk_penalty(equity: float, prev_equity: float, volatility: float = 0.02) -> float:
    # phat neu bien dong manh
    ret = abs(equity - prev_equity) / prev_equity if prev_equity else 0
    if ret > volatility * 2:
        return (ret - volatility*2) * 10
    return 0.0

def exposure_penalty(exposure_ratio: float, threshold: float = 1.5) -> float:
    if exposure_ratio > threshold:
        return (exposure_ratio - threshold) * 2
    return 0.0
