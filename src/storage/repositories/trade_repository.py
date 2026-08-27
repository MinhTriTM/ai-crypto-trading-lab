"""TradeRepository."""
from ...portfolio.trade import Trade

class TradeRepository:
    def __init__(self):
        self._trades: list[Trade] = []
    def save(self, trade: Trade):
        self._trades.append(trade)
    def get_by_account(self, account_id: str) -> list[Trade]:
        return [t for t in self._trades if t.order_id.startswith(account_id)]
    def get_by_symbol(self, symbol: str) -> list[Trade]:
        return [t for t in self._trades if t.symbol == symbol]
