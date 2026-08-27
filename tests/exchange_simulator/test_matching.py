from src.exchange_simulator.virtual_exchange import VirtualExchange
from src.portfolio.order import Order
from src.market.orderbook.orderbook import OrderBook

def test_market_order():
    ex = VirtualExchange()
    ob = OrderBook(symbol="BTCUSDT")
    ob.apply_snapshot([(67000,10)], [(67001,10)], 1)
    ex.update_orderbook(ob)
    order = Order(symbol="BTCUSDT", side="buy", type="market", qty=0.1)
    trades = ex.place_order(order)
    assert len(trades) == 1
    assert trades[0].qty > 0
