"""Leverage dimension."""
from dataclasses import dataclass, field

@dataclass
class LeverageDimension:
    leverages: list[float] = field(default_factory=lambda: [1,2,3,5])
    def values(self) -> list[float]:
        return self.leverages
