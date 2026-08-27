from src.ai.agent.trading_agent import TradingAgent
import numpy as np

def test_agent():
    agent = TradingAgent()
    state = np.random.randn(48).astype(np.float32)
    action = agent.decide(state)
    assert str(action) in ["HOLD", "LONG BTCUSDT 10.0% x2", "SHORT BTCUSDT 10.0% x2"] or "HOLD" in str(action)
