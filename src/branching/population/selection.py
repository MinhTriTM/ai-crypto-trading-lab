"""Selection."""
import random
import numpy as np
from ..branch_state import BranchState

def tournament_selection(states: list[BranchState], k: int = 3) -> BranchState:
    contenders = random.sample(states, min(k, len(states)))
    return max(contenders, key=lambda s: s.equity)

def roulette_selection(states: list[BranchState]) -> BranchState:
    equities = np.array([max(s.equity, 1) for s in states])
    probs = equities / equities.sum()
    return np.random.choice(states, p=probs)

def top_k_selection(states: list[BranchState], k: int = 10) -> list[BranchState]:
    return sorted(states, key=lambda s: s.equity, reverse=True)[:k]
