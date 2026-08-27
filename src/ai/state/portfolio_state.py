"""PortfolioState."""
from dataclasses import dataclass

@dataclass
class PortfolioState:
    equity: float = 1000.0
    free_balance: float = 1000.0
    total_exposure: float = 0.0
    num_positions: int = 0
    unrealized_pnl: float = 0.0
    drawdown: float = 0.0
    leverage: float = 1.0

    def to_vector(self) -> list[float]:
        return [self.equity/10000, self.free_balance/10000, self.total_exposure, self.unrealized_pnl/1000, self.drawdown, self.leverage/5]

    def is_risky(self) -> bool:
        return self.drawdown > 0.1 or self.leverage > 3
