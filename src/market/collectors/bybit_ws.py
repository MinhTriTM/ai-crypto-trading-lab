"""Bybit WebSocket collector."""
from .base_collector import BaseCollector
from src.market.events.market_event import MarketEvent
from typing import AsyncIterator
import json, websockets

class BybitWSCollector(BaseCollector):
    def __init__(self, symbols: list[str], ws_url: str = 'wss://stream.bybit.com/v5/public/spot'):
        super().__init__('bybit', symbols)
        self.ws_url = ws_url
        self._ws = None
    async def connect(self):
        self._ws = await websockets.connect(self.ws_url, ping_interval=20)
    async def subscribe(self):
        args = [f"publicTrade.{s}" for s in self.symbols] + [f"orderbook.50.{s}" for s in self.symbols]
        await self._ws.send(json.dumps({"op": "subscribe", "args": args}))
    async def stream(self) -> AsyncIterator[MarketEvent]:
        async for raw in self._ws:
            msg = json.loads(raw)
            yield MarketEvent.from_raw(msg, source='bybit')
