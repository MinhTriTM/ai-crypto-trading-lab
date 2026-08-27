"""Novelty - do do moi la."""
import numpy as np
from ..branch_state import BranchState

def novelty_score(state: BranchState, population: list[BranchState], k: int = 5) -> float:
    if len(population) < 2:
        return 1.0
    dists = [abs(state.equity - p.equity) for p in population if p.branch.id != state.branch.id]
    dists.sort()
    return float(np.mean(dists[:k])) if dists else 1.0

def novelty_search(states: list[BranchState], k: int = 5) -> list[tuple[BranchState, float]]:
    scored = [(s, novelty_score(s, states, k)) for s in states]
    return sorted(scored, key=lambda x: x[1], reverse=True)
