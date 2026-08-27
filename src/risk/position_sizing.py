"""Position sizing - Kelly, fixed fraction."""
import math

def kelly_position_size(win_rate: float, win_loss_ratio: float, fraction: float = 0.5) -> float:
    """Kelly fraction * reduce."""
    if win_loss_ratio == 0:
        return 0.0
    kelly = win_rate - (1-win_rate)/win_loss_ratio
    return max(0.0, kelly * fraction)

def fixed_fraction(equity: float, pct: float) -> float:
    return equity * pct

def volatility_sizing(equity: float, volatility: float, target_vol: float = 0.02) -> float:
    if volatility == 0:
        return equity * 0.1
    return equity * target_vol / volatility
