"""FeeEngine - tong hop fee."""
from .maker_taker import MakerTakerFee
from .funding import FundingFee
from src.portfolio.trade import Trade

class FeeEngine:
    def __init__(self, maker: float = 0.0002, taker: float = 0.0004):
        self.mt = MakerTakerFee(maker=maker, taker=taker)
        self.funding = FundingFee()

    def calculate(self, trade: Trade, is_maker: bool = False) -> float:
        notional = trade.price * trade.qty
        return self.mt.calculate(notional, is_maker)

    def funding_fee(self, notional: float, funding_rate: float, is_long: bool) -> float:
        return self.funding.apply(notional, is_long, funding_rate)
