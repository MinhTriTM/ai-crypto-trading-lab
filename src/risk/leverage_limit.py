"""Leverage limit."""
def allowed_leverage(equity: float, notional: float, max_leverage: float = 5) -> float:
    if equity <=0: return 1.0
    required = notional / equity
    return min(required, max_leverage)

def margin_required(notional: float, leverage: float) -> float:
    return notional / leverage
