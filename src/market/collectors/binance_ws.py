"""Binance WebSocket collector - thu thap trade/orderbook/funding that."""
import json
import asyncio
import websockets
from typing import AsyncIterator
from .base_collector import BaseCollector
from src.market.events.market_event import MarketEvent
from src.market.events.trade_event import TradeEvent
from src.market.events.orderbook_event import OrderbookEvent
from src.utils.logger import get_logger
logger = get_logger('market.binance')

class BinanceWSCollector(BaseCollector):
    def __init__(self, symbols: list[str], ws_url: str = 'wss://stream.binance.com:9443/ws'):
        super().__init__('binance', symbols)
        self.ws_url = ws_url
        self._ws = None

    async def connect(self):
        # Ho tro ca 2 dang: wss://stream.binance.com:9443/ws va wss://stream.binance.com:9443/stream
        # Dung combined stream: wss://stream.binance.com:9443/stream?streams=btcusdt@trade/btcusdt@depth@100ms
        streams = '/'.join([f"{s.lower()}@trade" for s in self.symbols] + [f"{s.lower()}@depth@100ms" for s in self.symbols])
        if streams:
            if self.ws_url.endswith('/ws'):
                base = self.ws_url[:-3]  # bo /ws
                url = f"{base}/stream?streams={streams}"
            elif '/stream' in self.ws_url:
                url = f"{self.ws_url}?streams={streams}" if '?' not in self.ws_url else self.ws_url
            else:
                url = f"{self.ws_url}/stream?streams={streams}"
        else:
            url = self.ws_url
        logger.info(f"Ket noi Binance WS: {url}")
        self._ws = await websockets.connect(url, ping_interval=20)

    async def subscribe(self):
        pass

    async def stream(self) -> AsyncIterator[MarketEvent]:
        assert self._ws is not None
        async for raw in self._ws:
            msg = json.loads(raw)
            data = msg.get('data', msg)
            if 'p' in data and 'q' in data:
                yield TradeEvent.from_binance(data)
            elif 'bids' in data or 'b' in data:
                yield OrderbookEvent.from_binance(data)
            else:
                yield MarketEvent.from_raw(data, source='binance')

    async def fetch_snapshot(self, symbol: str):
        url = f"https://api.binance.com/api/v3/depth?symbol={symbol}&limit=100"
        try:
            import aiohttp
            async with aiohttp.ClientSession() as s:
                async with s.get(url) as r:
                    return await r.json()
        except ImportError:
            # fallback requests
            import requests
            r = requests.get(url, timeout=5)
            return r.json()
