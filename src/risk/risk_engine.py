"""RiskEngine - kiem soat rui ro tong."""
from dataclasses import dataclass
from src.portfolio.virtual_account import VirtualAccount

@dataclass
class RiskEngine:
    max_position_pct: float = 0.25
    max_drawdown_pct: float = 0.15
    max_leverage: float = 5
    max_exposure: float = 2.0

    def can_open_position(self, account: VirtualAccount, notional: float, leverage: float) -> tuple[bool, str]:
        if leverage > self.max_leverage:
            return False, f"leverage {leverage} > max {self.max_leverage}"
        if notional / account.equity > self.max_position_pct:
            return False, f"position {notional/account.equity:.2%} > max {self.max_position_pct:.2%}"
        total_exposure = sum(p.notional for p in account.positions.values()) + notional
        if total_exposure / account.equity > self.max_exposure:
            return False, "tong exposure vuot nguong"
        # drawdown - dung equity hien tai vs initial lam peak hop ly
        # placeholder: neu chua co lich su, peak = max(initial, equity)
        peak = max(account.initial_balance, account.equity)
        # neu co lich su trade, dung max equity da dat (o day chua luu, tam dung peak nhu tren)
        dd = (peak - account.equity)/peak if peak else 0
        if dd > self.max_drawdown_pct:
            return False, f"drawdown {dd:.2%} > {self.max_drawdown_pct:.2%}"
        if account.is_bankrupt:
            return False, "account bankrupt"
        return True, "ok"

    def check_liquidation(self, account: VirtualAccount, prices: dict) -> list[str]:
        liquidated = []
        for sym, pos in list(account.positions.items()):
            price = prices.get(sym, pos.mark_price)
            if price and ((pos.is_long and price <= pos.liquidation_price()) or (not pos.is_long and price >= pos.liquidation_price())):
                liquidated.append(sym)
        return liquidated
