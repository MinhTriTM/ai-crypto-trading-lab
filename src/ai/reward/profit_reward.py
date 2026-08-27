"""Profit reward."""
def profit_reward(prev: float, curr: float) -> float:
    if prev == 0:
        return 0.0
    ret = (curr - prev) / prev
    # log shaping
    return ret * 100  # scale

def log_profit_reward(prev: float, curr: float) -> float:
    import math
    if prev <=0 or curr <=0:
        return 0.0
    return math.log(curr/prev) * 100
