from src.simulation.environment import TradingEnv

def test_env():
    env = TradingEnv()
    obs, _ = env.reset()
    assert obs.shape == (48,)
    obs2, reward, done, truncated, info = env.step(0)
    assert obs2.shape == (48,)
    assert "equity" in info
