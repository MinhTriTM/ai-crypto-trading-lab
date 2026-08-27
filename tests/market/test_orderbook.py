import pytest
from src.market.orderbook.orderbook import OrderBook

def test_orderbook_spread():
    ob = OrderBook(symbol="BTCUSDT")
    ob.apply_snapshot([(67000,1),(66999,2)], [(67001,1),(67002,2)], 1)
    assert ob.best_bid == 67000
    assert ob.best_ask == 67001
    assert ob.spread == 1
    assert ob.mid_price == 67000.5

def test_apply_delta():
    ob = OrderBook(symbol="BTCUSDT")
    ob.apply_snapshot([(67000,1)], [(67001,1)], 1)
    ob.apply_delta([(67000,0)], [(67001,2)], 2)
    assert 67000 not in ob.bids
    assert ob.asks[67001] == 2
