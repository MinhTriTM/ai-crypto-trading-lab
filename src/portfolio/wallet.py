"""Wallet - vi tong hop nhieu currency."""
from dataclasses import dataclass, field
from typing import Dict
from .balance import Balance

@dataclass
class Wallet:
    balances: Dict[str, Balance] = field(default_factory=dict)

    def get(self, currency: str) -> Balance:
        if currency not in self.balances:
            self.balances[currency] = Balance(currency=currency)
        return self.balances[currency]

    def deposit(self, currency: str, amount: float):
        self.get(currency).free += amount

    def withdraw(self, currency: str, amount: float) -> bool:
        b = self.get(currency)
        if b.free < amount:
            return False
        b.free -= amount
        return True

    def total_usdt(self, prices: Dict[str,float]) -> float:
        total = 0.0
        for cur, bal in self.balances.items():
            if cur == "USDT":
                total += bal.total
            else:
                total += bal.total * prices.get(cur+"USDT", 0)
        return total
