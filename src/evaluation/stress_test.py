"""StressTest."""
from src.simulation.scenario import Scenario, ScenarioType

class StressTest:
    def __init__(self, scenarios: list[Scenario] | None = None):
        if scenarios is None:
            self.scenarios = [
                Scenario(type=ScenarioType.FLASH_CRASH, volatility=0.05),
                Scenario(type=ScenarioType.VOLATILITY_SPIKE, volatility=0.04),
                Scenario(type=ScenarioType.BEAR, trend=-0.001, volatility=0.02),
                Scenario(type=ScenarioType.BULL, trend=0.001, volatility=0.02),
            ]
        else:
            self.scenarios = scenarios

    def run(self, env_fn, agent_fn) -> dict:
        results = {}
        for sc in self.scenarios:
            # placeholder: chay 10 episode moi scenario
            from src.evaluation.backtest import Backtest
            bt = Backtest()
            eps = bt.run(env_fn, agent_fn, n_episodes=10)
            avg = sum(e.return_pct for e in eps)/len(eps) if eps else 0
            results[sc.type.value] = {"avg_return": avg, "scenario": sc.type.value}
        return results
