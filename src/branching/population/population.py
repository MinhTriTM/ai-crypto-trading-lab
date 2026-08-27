"""Population - quan the cac branch."""
from dataclasses import dataclass, field
from ..branch import Branch
from ..branch_state import BranchState

@dataclass
class Population:
    branches: list[Branch] = field(default_factory=list)
    states: list[BranchState] = field(default_factory=list)
    generation: int = 0

    def add(self, branch: Branch, state: BranchState | None = None):
        self.branches.append(branch)
        if state:
            self.states.append(state)

    @property
    def size(self) -> int:
        return len(self.branches)

    @property
    def best(self) -> BranchState | None:
        if not self.states:
            return None
        return max(self.states, key=lambda s: s.equity)

    @property
    def avg_equity(self) -> float:
        return sum(s.equity for s in self.states)/len(self.states) if self.states else 0

    def stats(self) -> dict:
        return {"generation": self.generation, "size": self.size, "avg_equity": self.avg_equity, "best_equity": self.best.equity if self.best else 0}
