"""Target success rate."""
def target_success_rate(episodes, target: float = 10000) -> float:
    if not episodes: return 0.0
    return sum(1 for e in episodes if e.end_equity >= target) / len(episodes)

def time_to_target(episodes) -> float:
    times = [e.length for e in episodes if e.end_equity >= 10000]
    return sum(times)/len(times) if times else 0

def progress_to_target(episodes, initial: float = 1000, target: float = 10000) -> float:
    if not episodes: return 0.0
    progs = [(e.end_equity - initial)/(target-initial) for e in episodes]
    return sum(progs)/len(progs)
