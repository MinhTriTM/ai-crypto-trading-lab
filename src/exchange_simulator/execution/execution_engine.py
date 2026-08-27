"""ExecutionEngine - tinh gia khop thuc te gom spread/slippage."""
from src.portfolio.order import Order
from src.market.orderbook.orderbook import OrderBook

class ExecutionEngine:
    def __init__(self, slippage_bps: float = 5, spread_multiplier: float = 0.5):
        self.slippage_bps = slippage_bps
        self.spread_multiplier = spread_multiplier

    def effective_price(self, order: Order, ob: OrderBook) -> float:
        mid = ob.mid_price or 67000.0
        spread = ob.spread or 1.0
        # slippage dua tren spread va qty
        slip = spread * self.spread_multiplier * (1 + order.qty * 0.001)
        if order.side == "buy":
            return mid + slip/2 + mid * self.slippage_bps / 10000
        else:
            return mid - slip/2 - mid * self.slippage_bps / 10000
