"""Curriculum."""
from dataclasses import dataclass, field

@dataclass
class CurriculumStage:
    name: str
    market_regime: str
    difficulty: float
    timesteps: int

@dataclass
class Curriculum:
    stages: list[CurriculumStage] = field(default_factory=lambda: [
        CurriculumStage("easy", "sideways", 0.3, 1_000_000),
        CurriculumStage("medium", "mixed", 0.6, 3_000_000),
        CurriculumStage("hard", "volatile", 1.0, 6_000_000)
    ])
    current_idx: int = 0

    @property
    def current(self) -> CurriculumStage:
        return self.stages[self.current_idx]

    def advance(self) -> bool:
        if self.current_idx + 1 < len(self.stages):
            self.current_idx += 1
            return True
        return False

    def progress(self, timesteps: int) -> CurriculumStage:
        cum = 0
        for i, s in enumerate(self.stages):
            cum += s.timesteps
            if timesteps < cum:
                self.current_idx = i
                return s
        return self.stages[-1]
