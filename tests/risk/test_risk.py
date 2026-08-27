from src.risk.risk_engine import RiskEngine
from src.portfolio.virtual_account import VirtualAccount

def test_risk():
    engine = RiskEngine(max_position_pct=0.25)
    acc = VirtualAccount(initial_balance=1000)
    ok, msg = engine.can_open_position(acc, notional=200, leverage=2)
    assert ok
    ok, msg = engine.can_open_position(acc, notional=500, leverage=2)
    assert not ok
