"""Bankruptcy."""
from src.portfolio.virtual_account import VirtualAccount

def is_bankrupt(account: VirtualAccount, threshold_ratio: float = 0.1) -> bool:
    return account.equity <= account.initial_balance * threshold_ratio

def bankruptcy_probability(equity_curve: list[float], threshold: float) -> float:
    if not equity_curve: return 0.0
    breaches = sum(1 for v in equity_curve if v <= threshold)
    return breaches / len(equity_curve)

def should_stop_trading(account: VirtualAccount) -> bool:
    return is_bankrupt(account) or account.equity < 0
