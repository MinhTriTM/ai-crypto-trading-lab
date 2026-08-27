"""Survival rate."""
def survival_rate(episodes) -> float:
    if not episodes: return 0.0
    survived = sum(1 for e in episodes if not getattr(e, 'done_reason', '') == 'bankrupt' and e.end_equity > e.start_equity*0.1)
    return survived / len(episodes)

def bankruptcy_rate(episodes) -> float:
    return 1 - survival_rate(episodes)

def target_success_rate(episodes, target: float = 10000, initial: float = 1000) -> float:
    if not episodes: return 0.0
    hit = sum(1 for e in episodes if e.end_equity >= target)
    return hit / len(episodes)
