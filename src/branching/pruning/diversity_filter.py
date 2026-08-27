"""DiversityFilter - dam bao da dang."""
import numpy as np
from ..branch_state import BranchState

class DiversityFilter:
    def __init__(self, max_per_asset: int = 5, max_per_direction: int = 10):
        self.max_per_asset = max_per_asset
        self.max_per_direction = max_per_direction

    def filter(self, states: list[BranchState]) -> list[BranchState]:
        # gioi han so branch moi asset/direction
        counts_asset: dict[str,int] = {}
        counts_dir: dict[str,int] = {}
        out: list[BranchState] = []
        for s in states:
            asset = s.branch.symbol
            direction = s.branch.action
            if counts_asset.get(asset,0) >= self.max_per_asset:
                continue
            if counts_dir.get(direction,0) >= self.max_per_direction:
                continue
            out.append(s)
            counts_asset[asset] = counts_asset.get(asset,0)+1
            counts_dir[direction] = counts_dir.get(direction,0)+1
        return out

    def novelty_filter(self, states: list[BranchState], threshold: float = 0.1) -> list[BranchState]:
        # loai branch qua giong nhau dua tren equity
        seen = []
        out = []
        for s in states:
            if all(abs(s.equity - v) > threshold*100 for v in seen):
                out.append(s)
                seen.append(s.equity)
        return out
