"""BranchPruner - cat tia branch kem."""
from ..branch_state import BranchState
from .scorer import BranchScorer

class BranchPruner:
    def __init__(self, keep_ratio: float = 0.3, min_keep: int = 10):
        self.keep_ratio = keep_ratio
        self.min_keep = min_keep
        self.scorer = BranchScorer()

    def prune(self, states: list[BranchState]) -> list[BranchState]:
        if len(states) <= self.min_keep:
            return states
        ranked = self.scorer.rank(states)
        keep_n = max(self.min_keep, int(len(states) * self.keep_ratio))
        # danh dau pruned
        for s in ranked[keep_n:]:
            s.branch.status = "pruned"
        return ranked[:keep_n]

    def prune_by_threshold(self, states: list[BranchState], threshold: float = 0.0) -> list[BranchState]:
        kept = [s for s in states if self.scorer.score(s) >= threshold]
        return kept if kept else states[:self.min_keep]
