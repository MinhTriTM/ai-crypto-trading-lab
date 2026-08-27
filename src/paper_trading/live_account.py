"""LiveAccount - tai khoan paper realtime."""
from dataclasses import dataclass, field
from src.portfolio.virtual_account import VirtualAccount
import time

@dataclass
class LiveAccount(VirtualAccount):
    created_at: int = field(default_factory=lambda: int(time.time()*1000))
    last_update: int = 0
    total_trades: int = 0

    def update_mark_price(self, prices: dict[str,float]):
        for sym, pos in self.positions.items():
            if sym in prices:
                pos.mark_price = prices[sym]
                self.last_update = int(time.time()*1000)

    @property
    def unrealized(self) -> float:
        return sum(p.unrealized_pnl(p.mark_price or p.entry_price) for p in self.positions.values())
