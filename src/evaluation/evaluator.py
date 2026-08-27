"""Evaluator - tong hop danh gia."""
from dataclasses import dataclass
from typing import List
from .backtest import Backtest
from .metrics.return_metrics import return_metrics
from .metrics.sharpe import sharpe_ratio
from .metrics.drawdown import max_drawdown
from .metrics.win_rate import win_rate
from .metrics.survival_rate import survival_rate

@dataclass
class Evaluator:
    backtest: Backtest = None

    def __post_init__(self):
        if self.backtest is None:
            from .backtest import Backtest
            self.backtest = Backtest()

    def evaluate(self, episodes: list) -> dict:
        equities = [e.end_equity for e in episodes]
        returns = [e.return_pct for e in episodes]
        return {
            "episodes": len(episodes),
            "avg_return": sum(returns)/len(returns) if returns else 0,
            "sharpe": sharpe_ratio(returns),
            "max_drawdown": max_drawdown(equities),
            "win_rate": win_rate(returns),
            "survival_rate": survival_rate(episodes),
            "avg_equity": sum(equities)/len(equities) if equities else 0
        }

    def compare(self, runs: dict[str, list]) -> dict:
        return {name: self.evaluate(eps) for name, eps in runs.items()}
