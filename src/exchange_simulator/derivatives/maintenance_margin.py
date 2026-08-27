"""Maintenance margin."""
from dataclasses import dataclass

@dataclass
class MaintenanceMargin:
    rate: float = 0.005  # 0.5%

    def required(self, notional: float) -> float:
        return notional * self.rate

    def is_margin_call(self, equity: float, notional: float) -> bool:
        return equity < self.required(notional) * 2

    def is_liquidation(self, equity: float, notional: float) -> bool:
        return equity < self.required(notional)
