from src.portfolio.virtual_account import VirtualAccount
from src.portfolio.trade import Trade

def test_virtual_account():
    acc = VirtualAccount(initial_balance=1000, target=10000)
    assert acc.equity == 1000
    trade = Trade(symbol="BTCUSDT", side="buy", price=67000, qty=0.01, fee=1.0)
    acc.apply_trade(trade)
    assert len(acc.trades) == 1
    assert acc.balances["USDT"].free < 1000
