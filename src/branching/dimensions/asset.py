"""Asset dimension."""
from dataclasses import dataclass, field

@dataclass
class AssetDimension:
    assets: list[str] = field(default_factory=lambda: ["BTCUSDT","ETHUSDT","SOLUSDT","BNBUSDT","AVAXUSDT"])
    def values(self) -> list[str]:
        return self.assets
    def sample(self) -> str:
        import random
        return random.choice(self.assets)
