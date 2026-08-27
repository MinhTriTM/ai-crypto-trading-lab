"""ExitTime dimension."""
from dataclasses import dataclass, field
import random

@dataclass
class ExitTimeDimension:
    exits_ms: list[int] = field(default_factory=lambda: [100, 1000, 10000, 60000, 300000])
    def values(self) -> list[int]:
        return self.exits_ms
    def sample(self) -> int:
        return random.choice(self.exits_ms)
