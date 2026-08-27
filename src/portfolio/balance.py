"""Balance."""
from dataclasses import dataclass

@dataclass
class Balance:
    currency: str = "USDT"
    free: float = 0.0
    locked: float = 0.0

    @property
    def total(self) -> float:
        return self.free + self.locked

    def lock(self, amount: float) -> bool:
        if self.free < amount:
            return False
        self.free -= amount
        self.locked += amount
        return True

    def unlock(self, amount: float):
        self.locked -= amount
        self.free += amount
