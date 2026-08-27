"""Base collector - lop co so cho moi collector san."""
import asyncio
from abc import ABC, abstractmethod
from typing import AsyncIterator
from src.market.events.market_event import MarketEvent

class BaseCollector(ABC):
    """Collector bat dong bo, tu reconnect."""
    def __init__(self, exchange: str, symbols: list[str]):
        self.exchange = exchange
        self.symbols = symbols
        self._running = False

    @abstractmethod
    async def connect(self): ...
    @abstractmethod
    async def subscribe(self): ...
    @abstractmethod
    async def stream(self) -> AsyncIterator[MarketEvent]: ...

    async def start(self):
        self._running = True
        backoff = 1.0
        while self._running:
            try:
                await self.connect()
                await self.subscribe()
                async for event in self.stream():
                    yield event
                backoff = 1.0
            except Exception as e:
                print(f"[{self.exchange}] loi: {e}, reconnect sau {backoff}s")
                await asyncio.sleep(backoff)
                backoff = min(backoff * 2, 30)

    async def stop(self):
        self._running = False
