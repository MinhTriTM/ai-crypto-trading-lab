"""Difficulty."""
def difficulty_by_volatility(vol: float) -> float:
    if vol < 0.01: return 0.3
    if vol < 0.03: return 0.6
    return 1.0

def difficulty_by_drawdown(dd: float) -> float:
    return min(1.0, dd * 5)

def adjust_difficulty(current: float, success_rate: float, target: float = 0.6) -> float:
    if success_rate > target + 0.1:
        return min(1.0, current + 0.1)
    if success_rate < target - 0.1:
        return max(0.1, current - 0.1)
    return current
