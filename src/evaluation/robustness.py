"""Robustness."""
import numpy as np

class Robustness:
    def test_latency(self, env_fn, agent_fn, latencies: list[float] = [1,5,10,20]) -> dict:
        out = {}
        for lat in latencies:
            # placeholder: gia lap latency bang cach delay
            eps = []
            from src.evaluation.backtest import Backtest
            bt = Backtest()
            eps = bt.run(env_fn, agent_fn, n_episodes=20)
            out[f"latency_{lat}ms"] = sum(e.return_pct for e in eps)/len(eps) if eps else 0
        return out

    def test_slippage(self, env_fn, agent_fn, slippages: list[float] = [1,5,10]) -> dict:
        out = {}
        for s in slippages:
            from src.evaluation.backtest import Backtest
            bt = Backtest()
            eps = bt.run(env_fn, agent_fn, n_episodes=20)
            out[f"slippage_{s}bps"] = sum(e.return_pct for e in eps)/len(eps) if eps else 0
        return out

    def noise_test(self, returns: list[float], noise: float = 0.01) -> dict:
        arr = np.array(returns)
        noisy = arr + np.random.randn(len(arr))*noise
        return {"original_mean": float(arr.mean()), "noisy_mean": float(noisy.mean()), "degradation": float(arr.mean()-noisy.mean())}
