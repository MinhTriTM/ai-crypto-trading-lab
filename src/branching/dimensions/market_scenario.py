"""MarketScenario dimension."""
from dataclasses import dataclass, field

@dataclass
class MarketScenarioDimension:
    scenarios: list[str] = field(default_factory=lambda: ["bull","bear","sideways","flash_crash","volatility_spike"])
    def values(self) -> list[str]:
        return self.scenarios
