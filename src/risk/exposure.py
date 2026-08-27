"""Exposure."""
from src.portfolio.virtual_account import VirtualAccount

def total_exposure(account: VirtualAccount) -> float:
    return sum(p.notional for p in account.positions.values())

def exposure_ratio(account: VirtualAccount) -> float:
    tot = total_exposure(account)
    return tot / account.equity if account.equity else 0

def asset_exposure(account: VirtualAccount, symbol: str) -> float:
    p = account.positions.get(symbol)
    return p.notional / account.equity if p and account.equity else 0
