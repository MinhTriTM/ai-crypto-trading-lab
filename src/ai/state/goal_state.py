"""GoalState - muc tieu tai khoan."""
from dataclasses import dataclass

@dataclass
class GoalState:
    initial: float = 1000.0
    target: float = 10000.0
    current: float = 1000.0
    steps: int = 0
    max_steps: int = 10000

    @property
    def progress(self) -> float:
        return (self.current - self.initial) / (self.target - self.initial) if self.target != self.initial else 0

    @property
    def is_done(self) -> bool:
        return self.current >= self.target or self.current <= self.initial*0.1 or self.steps >= self.max_steps

    @property
    def reward_shaping(self) -> float:
        return self.progress
