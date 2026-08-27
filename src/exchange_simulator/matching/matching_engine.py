"""MatchingEngine - khop lenh."""
from typing import List
from src.portfolio.order import Order
from src.portfolio.trade import Trade
from src.market.orderbook.orderbook import OrderBook
import uuid, time

class MatchingEngine:
    def match(self, order: Order, ob: OrderBook, effective_price: float) -> List[Trade]:
        trades: List[Trade] = []
        if order.type == "market":
            # market order khop ngay tai effective_price
            qty = order.qty
            # partial fill mo phong
            filled = qty * (0.95 + 0.05 * (hash(order.id) % 10)/10)
            trades.append(Trade(
                id=str(uuid.uuid4()),
                order_id=order.id,
                symbol=order.symbol,
                side=order.side,
                price=effective_price,
                qty=filled,
                timestamp=int(time.time()*1000),
                fee=0.0
            ))
            if filled < qty:
                # phan con lai pending
                order.filled_qty = filled
                order.status = "partially_filled"
            else:
                order.status = "filled"
        elif order.type == "limit":
            # limit: chi khop neu gia dat
            can_fill = (order.side=="buy" and effective_price <= order.price) or (order.side=="sell" and effective_price >= order.price)
            if can_fill:
                trades.append(Trade(
                    id=str(uuid.uuid4()),
                    order_id=order.id,
                    symbol=order.symbol,
                    side=order.side,
                    price=order.price,
                    qty=order.qty,
                    timestamp=int(time.time()*1000)
                ))
                order.status = "filled"
            else:
                order.status = "open"
        return trades
