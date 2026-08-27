from src.market.features.feature_engine import FeatureEngine
from src.market.orderbook.orderbook import OrderBook

def test_feature_engine():
    fe = FeatureEngine()
    ob = OrderBook(symbol="BTCUSDT")
    ob.apply_snapshot([(67000,1)], [(67001,1)], 1)
    for i in range(10):
        fe.update(67000+i, 1.0, ob)
    vec = fe.build()
    assert vec.shape == (32,)
