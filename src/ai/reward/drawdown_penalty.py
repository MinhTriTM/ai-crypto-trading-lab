"""Drawdown penalty."""
def drawdown_penalty(dd: float, threshold: float = 0.05) -> float:
    if dd <= threshold:
        return 0.0
    return (dd - threshold) * 20

def max_drawdown_penalty(mdd: float) -> float:
    return mdd * 10
