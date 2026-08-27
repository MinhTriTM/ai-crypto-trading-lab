"""Leverage - don bay."""
from dataclasses import dataclass

@dataclass
class LeverageEngine:
    max_leverage: int = 10
    default: int = 2

    def notional(self, margin: float, leverage: float) -> float:
        lev = min(leverage, self.max_leverage)
        return margin * lev

    def required_margin(self, notional: float, leverage: float) -> float:
        return notional / leverage

    def validate(self, leverage: float) -> bool:
        return 1 <= leverage <= self.max_leverage
