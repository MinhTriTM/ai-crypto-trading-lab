"""Coinbase WebSocket collector."""
from .base_collector import BaseCollector
from src.market.events.market_event import MarketEvent
from typing import AsyncIterator
import json, websockets

class CoinbaseWSCollector(BaseCollector):
    def __init__(self, symbols: list[str], ws_url: str = 'wss://ws-feed.exchange.coinbase.com'):
        super().__init__('coinbase', symbols)
        self.ws_url = ws_url
        self._ws = None
    async def connect(self):
        self._ws = await websockets.connect(self.ws_url, ping_interval=20)
    async def subscribe(self):
        await self._ws.send(json.dumps({"type": "subscribe","product_ids": self.symbols,"channels": ["ticker","level2","matches"]}))
    async def stream(self) -> AsyncIterator[MarketEvent]:
        async for raw in self._ws:
            msg = json.loads(raw)
            yield MarketEvent.from_raw(msg, source='coinbase')
