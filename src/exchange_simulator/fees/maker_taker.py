"""Maker/Taker fee."""
from dataclasses import dataclass

@dataclass
class MakerTakerFee:
    maker: float = 0.0002
    taker: float = 0.0004

    def get(self, is_maker: bool) -> float:
        return self.maker if is_maker else self.taker

    def calculate(self, notional: float, is_maker: bool = False) -> float:
        return notional * self.get(is_maker)
