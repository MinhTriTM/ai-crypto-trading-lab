"""TimeOffset dimension."""
import random
from dataclasses import dataclass

@dataclass
class TimeOffsetDimension:
    offsets: list[int] = None
    def __post_init__(self):
        if self.offsets is None:
            self.offsets = [0, 7, 10, 50, 100]
    def values(self) -> list[int]:
        return self.offsets
    def sample(self) -> int:
        return random.choice(self.offsets)
