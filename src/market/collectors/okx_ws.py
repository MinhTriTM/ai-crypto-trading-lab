"""OKX WebSocket collector."""
from .base_collector import BaseCollector
from src.market.events.market_event import MarketEvent
from typing import AsyncIterator
import json, websockets

class OkxWSCollector(BaseCollector):
    def __init__(self, symbols: list[str], ws_url: str = 'wss://ws.okx.com:8443/ws/v5/public'):
        super().__init__('okx', symbols)
        self.ws_url = ws_url
        self._ws = None
    async def connect(self):
        self._ws = await websockets.connect(self.ws_url, ping_interval=20)
    async def subscribe(self):
        args = [{"channel": "trades", "instId": s} for s in self.symbols]
        await self._ws.send(json.dumps({"op": "subscribe", "args": args}))
    async def stream(self) -> AsyncIterator[MarketEvent]:
        async for raw in self._ws:
            msg = json.loads(raw)
            yield MarketEvent.from_raw(msg, source='okx')
