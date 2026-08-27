"""Orderbook imbalance."""
from src.market.orderbook.orderbook import OrderBook

def book_imbalance(ob: OrderBook, levels: int = 5) -> float:
    bids, asks = ob.depth(levels)
    bv = sum(q for _,q in bids)
    av = sum(q for _,q in asks)
    tot = bv+av
    return (bv-av)/tot if tot else 0.0

def weighted_mid_price(ob: OrderBook) -> float:
    bids, asks = ob.depth(1)
    if not bids or not asks: return ob.mid_price
    bp,bq = bids[0]; ap,aq = asks[0]
    return (bp*aq + ap*bq)/(bq+aq) if (bq+aq) else ob.mid_price
