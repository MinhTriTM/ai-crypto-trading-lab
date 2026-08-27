"""BranchExecutor - chay branch qua simulator."""
from typing import List
from .branch import Branch
from .branch_state import BranchState
from src.portfolio.virtual_account import VirtualAccount
from src.exchange_simulator.virtual_exchange import VirtualExchange
from src.ai.actions.long import LongAction
from src.ai.actions.short import ShortAction
from src.ai.actions.hold import HoldAction

class BranchExecutor:
    def __init__(self, exchange: VirtualExchange):
        self.exchange = exchange

    def execute(self, branch: Branch, market_price: float) -> BranchState:
        # tao account ao cho branch
        acc = VirtualAccount(initial_balance=branch.capital, target=branch.target)
        # chuyen branch action thanh order
        action = self._to_action(branch)
        if action and not action.is_hold:
            order = action.to_order(acc.equity, market_price)
            if order:
                trades = self.exchange.place_order(order)
                for t in trades:
                    acc.apply_trade(t)
        # tra ve state
        return BranchState(branch=branch, equity=acc.equity, timestamp=0)

    def execute_batch(self, branches: List[Branch], market_price: float) -> List[BranchState]:
        return [self.execute(b, market_price) for b in branches]

    def _to_action(self, branch: Branch):
        if branch.action == "LONG":
            return LongAction(symbol=branch.symbol, size_pct=branch.position_pct, leverage=branch.leverage)
        elif branch.action == "SHORT":
            return ShortAction(symbol=branch.symbol, size_pct=branch.position_pct, leverage=branch.leverage)
        elif branch.action in ("HOLD","WAIT_10MS"):
            return HoldAction()
        elif "CLOSE" in branch.action:
            # dong vi the -> short/long nguoc
            return HoldAction()
        elif "ADD" in branch.action:
            return LongAction(symbol=branch.symbol, size_pct=0.05, leverage=branch.leverage)
        elif branch.action == "REVERSE":
            return ShortAction(symbol=branch.symbol, size_pct=branch.position_pct, leverage=branch.leverage)
        return HoldAction()
