"""Account - tai khoan co ban."""
from dataclasses import dataclass, field
from typing import Dict
from .balance import Balance
from .position import Position

@dataclass
class Account:
    id: str
    balances: Dict[str, Balance] = field(default_factory=dict)
    positions: Dict[str, Position] = field(default_factory=dict)

    def equity(self, prices: Dict[str,float]) -> float:
        total = sum(b.total for b in self.balances.values())
        for sym, pos in self.positions.items():
            price = prices.get(sym, pos.entry_price)
            total += pos.unrealized_pnl(price)
        return total
