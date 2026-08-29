"""Liquidation."""
from dataclasses import dataclass, field
from .maintenance_margin import MaintenanceMargin

@dataclass
class LiquidationEngine:
    mm: MaintenanceMargin = field(default_factory=MaintenanceMargin)
    fee_rate: float = 0.001

    def check(self, equity: float, notional: float) -> bool:
        return self.mm.is_liquidation(equity, notional)

    def liquidate_price(self, entry: float, leverage: float, is_long: bool) -> float:
        # Don gian: gia thanh ly cach entry ~ 1/leverage
        move = entry / leverage * 0.9
        return entry - move if is_long else entry + move

    def fee(self, notional: float) -> float:
        return notional * self.fee_rate
