"""Target reward."""
def target_reward(is_target: bool, is_bankrupt: bool) -> float:
    if is_target:
        return 10.0
    if is_bankrupt:
        return -10.0
    return 0.0

def progress_reward(progress: float) -> float:
    return progress * 2
