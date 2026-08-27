"""PositionSize dimension."""
from dataclasses import dataclass, field

@dataclass
class PositionSizeDimension:
    sizes: list[float] = field(default_factory=lambda: [5,10,17,20,25])  # %
    def values(self) -> list[float]:
        return self.sizes
    def sample(self) -> float:
        import random
        return random.choice(self.sizes)
