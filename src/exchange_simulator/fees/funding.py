"""Funding fee cho futures."""
from dataclasses import dataclass

@dataclass
class FundingFee:
    rate: float = 0.0001  # 0.01% per 8h

    def periodic_fee(self, notional: float) -> float:
        return notional * self.rate

    def apply(self, position_notional: float, is_long: bool, funding_rate: float) -> float:
        # long tra funding neu rate duong
        fee = position_notional * funding_rate
        return -fee if is_long else fee
