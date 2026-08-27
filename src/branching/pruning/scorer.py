"""Scorer - cham diem branch."""
from ..branch_state import BranchState

class BranchScorer:
    def score(self, state: BranchState) -> float:
        # diem dua tren pnl, progress, drawdown
        equity = state.equity
        branch = state.branch
        ret = (equity - branch.capital) / branch.capital if branch.capital else 0
        progress = state.progress
        # thuong return, phat drawdown
        score = ret * 10 + progress * 5
        if equity < branch.capital * 0.5:
            score -= 5  # gan pha san
        return score

    def rank(self, states: list[BranchState]) -> list[BranchState]:
        return sorted(states, key=lambda s: self.score(s), reverse=True)
