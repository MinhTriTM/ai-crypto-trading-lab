"""Spread model."""
from src.market.orderbook.orderbook import OrderBook

def effective_spread(ob: OrderBook, use_real: bool = True, min_bps: float = 1.0) -> float:
    if use_real and ob.spread_bps > 0:
        return max(ob.spread, ob.mid_price * min_bps / 10000)
    return ob.mid_price * min_bps / 10000

def spread_cost(qty: float, spread: float) -> float:
    return qty * spread / 2
