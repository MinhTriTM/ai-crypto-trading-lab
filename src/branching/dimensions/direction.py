"""Direction dimension."""
from dataclasses import dataclass, field

@dataclass
class DirectionDimension:
    directions: list[str] = field(default_factory=lambda: ["LONG","SHORT","HOLD"])
    def values(self) -> list[str]:
        return self.directions
