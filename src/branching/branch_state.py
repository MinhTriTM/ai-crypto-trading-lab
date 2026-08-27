"""BranchState - trang thai cua branch tai 1 thoi diem."""
from dataclasses import dataclass, field
import numpy as np
from .branch import Branch

@dataclass
class BranchState:
    branch: Branch
    market_state: np.ndarray = field(default_factory=lambda: np.zeros(48))
    equity: float = 1000.0
    timestamp: int = 0
    step: int = 0

    @property
    def progress(self) -> float:
        return (self.equity - self.branch.capital) / (self.branch.target - self.branch.capital) if self.branch.target != self.branch.capital else 0

    def clone(self) -> "BranchState":
        import copy
        return copy.deepcopy(self)
