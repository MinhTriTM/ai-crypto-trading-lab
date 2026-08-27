"""VirtualAccount - tai khoan ao doc lap, khong lien ket san that."""
from dataclasses import dataclass, field
from typing import Dict, List
import uuid, time
from .balance import Balance
from .position import Position
from .order import Order
from .trade import Trade
from .pnl import PnL

@dataclass
class VirtualAccount:
    """Moi account co so du, vi the, PnL rieng."""
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    initial_balance: float = 1000.0
    target: float = 10000.0
    balances: Dict[str, Balance] = field(default_factory=dict)
    positions: Dict[str, Position] = field(default_factory=dict)
    orders: List[Order] = field(default_factory=list)
    trades: List[Trade] = field(default_factory=list)
    pnl: PnL = field(default_factory=PnL)

    def __post_init__(self):
        if "USDT" not in self.balances:
            self.balances["USDT"] = Balance(currency="USDT", free=self.initial_balance, locked=0.0)

    @property
    def equity(self) -> float:
        bal = self.balances["USDT"].total if "USDT" in self.balances else 0
        unreal = sum(p.unrealized_pnl(p.mark_price or p.entry_price) for p in self.positions.values())
        return bal + unreal

    def can_afford(self, cost: float) -> bool:
        return self.balances["USDT"].free >= cost

    def apply_trade(self, trade: Trade):
        self.trades.append(trade)
        # cap nhat position
        pos = self.positions.get(trade.symbol)
        if not pos:
            pos = Position(symbol=trade.symbol, side=trade.side, qty=trade.qty, entry_price=trade.price, mark_price=trade.price, leverage=1)
            self.positions[trade.symbol] = pos
        else:
            # don gian: trung binh gia
            total_qty = pos.qty + trade.qty if trade.side==pos.side else pos.qty - trade.qty
            if total_qty == 0:
                # dong vi the
                realized = pos.unrealized_pnl(trade.price)
                self.pnl.realized += realized
                self.balances["USDT"].free += realized
                del self.positions[trade.symbol]
            else:
                pos.qty = abs(total_qty)
                if trade.side == pos.side:
                    pos.entry_price = (pos.entry_price*pos.qty + trade.price*trade.qty)/(pos.qty+trade.qty)
        # tru fee
        self.balances["USDT"].free -= trade.fee
        self.pnl.fees += trade.fee

    @property
    def is_bankrupt(self) -> bool:
        return self.equity <= self.initial_balance * 0.1

    @property
    def is_target_reached(self) -> bool:
        return self.equity >= self.target

    def to_dict(self):
        return {"id": self.id, "equity": self.equity, "initial": self.initial_balance, "target": self.target, "positions": len(self.positions), "trades": len(self.trades)}
