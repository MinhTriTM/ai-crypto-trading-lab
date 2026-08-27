"""Reconstruction - tai tao orderbook tu snapshot + delta."""
from .orderbook import OrderBook
from .snapshot import Snapshot
from .delta import Delta
from src.utils.logger import get_logger
logger = get_logger('market.reconstruction')

class OrderBookReconstructor:
    def __init__(self, symbol: str):
        self.symbol = symbol
        self.book = OrderBook(symbol=symbol)
        self._initialized = False
        self._buffer: list[Delta] = []

    def init_snapshot(self, snapshot: Snapshot):
        self.book.apply_snapshot(snapshot.bids, snapshot.asks, snapshot.last_update_id)
        self._initialized = True
        for d in sorted(self._buffer, key=lambda x: x.first_update_id):
            if d.final_update_id > self.book.last_update_id:
                self.apply_delta(d)
        self._buffer.clear()
        logger.info(f"[{self.symbol}] snapshot init id={snapshot.last_update_id}")

    def apply_delta(self, delta: Delta):
        if not self._initialized:
            self._buffer.append(delta)
            return False
        if not delta.is_valid(self.book.last_update_id):
            logger.warning(f"[{self.symbol}] delta gap: last={self.book.last_update_id} delta U={delta.first_update_id} u={delta.final_update_id}")
            return False
        self.book.apply_delta(delta.bids, delta.asks, delta.final_update_id)
        self.book.timestamp = delta.timestamp
        return True
