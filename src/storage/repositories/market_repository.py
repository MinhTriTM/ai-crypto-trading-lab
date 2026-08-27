"""MarketRepository."""
from ..clickhouse import Clickhouse

class MarketRepository:
    def __init__(self, ch: Clickhouse | None = None):
        self.ch = ch or Clickhouse()
    def save_trades(self, trades: list[dict]):
        self.ch.insert_trades(trades)
    def get_trades(self, symbol: str, start_ms: int, end_ms: int):
        return self.ch.query(f"SELECT * FROM market_data.trades WHERE symbol='{symbol}' AND timestamp BETWEEN {start_ms} AND {end_ms}")
