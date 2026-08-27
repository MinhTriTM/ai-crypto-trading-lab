"""WalkForward."""
from dataclasses import dataclass

@dataclass
class WalkForwardConfig:
    train_days: int = 30
    test_days: int = 7
    step_days: int = 7
    n_splits: int = 4

class WalkForward:
    def __init__(self, config: WalkForwardConfig = WalkForwardConfig()):
        self.cfg = config

    def splits(self, total_days: int) -> list[tuple[int,int,int,int]]:
        # tra ve list (train_start, train_end, test_start, test_end) tinh bang day index
        out = []
        start = 0
        for _ in range(self.cfg.n_splits):
            train_end = start + self.cfg.train_days
            test_end = train_end + self.cfg.test_days
            if test_end > total_days:
                break
            out.append((start, train_end, train_end, test_end))
            start += self.cfg.step_days
        return out

    def evaluate(self, splits, eval_fn):
        results = []
        for s in splits:
            results.append(eval_fn(s))
        return results
