"""VirtualExchange - san giao dich mo phong trung tam."""
from dataclasses import dataclass, field
from typing import Dict, List
from src.market.orderbook.orderbook import OrderBook
from src.portfolio.order import Order
from src.portfolio.trade import Trade
from .matching.matching_engine import MatchingEngine
from .execution.execution_engine import ExecutionEngine
from .fees.fee_engine import FeeEngine
from .derivatives.leverage import LeverageEngine
import time, uuid

@dataclass
class VirtualExchange:
    """Nhan order tu AI, khop dua tren orderbook that, tinh fee/slippage/latency."""
    matching: MatchingEngine = field(default_factory=MatchingEngine)
    execution: ExecutionEngine = field(default_factory=ExecutionEngine)
    fees: FeeEngine = field(default_factory=FeeEngine)
    leverage: LeverageEngine = field(default_factory=LeverageEngine)
    orderbooks: Dict[str, OrderBook] = field(default_factory=dict)

    def update_orderbook(self, ob: OrderBook):
        self.orderbooks[ob.symbol] = ob

    def place_order(self, order: Order) -> List[Trade]:
        ob = self.orderbooks.get(order.symbol)
        if not ob:
            # tao orderbook gia neu chua co
            ob = OrderBook(symbol=order.symbol)
            ob.apply_snapshot([(67000,1)], [(67001,1)], 0)
        # execution: tinh slippage/spread/latency
        eff_price = self.execution.effective_price(order, ob)
        # matching
        trades = self.matching.match(order, ob, eff_price)
        # fees
        for t in trades:
            t.fee = self.fees.calculate(t)
        return trades

    def get_price(self, symbol: str) -> float:
        ob = self.orderbooks.get(symbol)
        return ob.mid_price if ob else 67000.0

    def mark_price(self, symbol: str) -> float:
        return self.get_price(symbol)
