"""
MultiExchangeCollector — tự fallback Binance -> Vision -> OKX -> Coinbase khi bị chặn 451.
Dùng cho Colab US nơi api.binance.com/stream.binance.com bị chặn nhưng data-api.binance.vision/okx/coinbase vẫn OK.
"""
import requests
import asyncio
import json
from typing import AsyncIterator
from .base_collector import BaseCollector
from src.market.events.market_event import MarketEvent
from src.market.events.trade_event import TradeEvent
from src.utils.logger import get_logger

logger = get_logger('market.multi')

# Thử REST theo thứ tự: vision -> okx -> coinbase
def fetch_price_fallback(symbol="BTCUSDT"):
    # symbol BTCUSDT -> BTC-USDT cho OKX, BTC-USD cho Coinbase
    urls = [
        ("vision", f"https://data-api.binance.vision/api/v3/ticker/price?symbol={symbol}"),
        ("okx", f"https://www.okx.com/api/v5/market/ticker?instId={symbol.replace('USDT','-USDT')}"),
        ("coinbase", f"https://api.exchange.coinbase.com/products/{symbol.replace('USDT','-USD')}/ticker"),
    ]
    for name, url in urls:
        try:
            r = requests.get(url, timeout=5)
            if r.status_code == 200:
                data = r.json()
                # Chuẩn hóa
                if name == "vision":
                    price = float(data["price"])
                    logger.info(f"Price via vision {symbol}={price}")
                    return price, name
                elif name == "okx":
                    price = float(data["data"][0]["last"])
                    logger.info(f"Price via okx {symbol}={price}")
                    return price, name
                elif name == "coinbase":
                    price = float(data["price"])
                    logger.info(f"Price via coinbase {symbol}={price}")
                    return price, name
        except Exception as e:
            logger.warning(f"Price fallback {name} fail: {e}")
            continue
    raise RuntimeError("All price fallbacks failed")

class MultiExchangeCollector(BaseCollector):
    """
    Tự chọn collector còn sống:
    - Ưu tiên Binance WS nếu không 451
    - Nếu 451 thì fallback OKX WS (wss://ws.okx.com:8443/ws/v5/public)
    """
    def __init__(self, symbols: list[str], preferred="binance"):
        super().__init__("multi", symbols)
        self.preferred = preferred
        self._active = None
        self._ws = None

    async def connect(self):
        # Thử Binance trước
        if self.preferred == "binance":
            try:
                from .binance_ws import BinanceWSCollector
                c = BinanceWSCollector(self.symbols)
                await c.connect()
                # Test nhanh xem có bị 451 không bằng cách thử recv 1 msg với timeout 3s
                # Nếu handshake đã fail thì exception đã raise ở connect
                self._active = c
                self._ws = c._ws
                logger.info("Multi: dùng Binance")
                return
            except Exception as e:
                if "451" in str(e) or "InvalidStatus" in str(e) or "restricted" in str(e).lower():
                    logger.warning(f"Binance bị chặn 451, fallback OKX: {e}")
                else:
                    logger.warning(f"Binance fail, fallback OKX: {e}")
        # Fallback OKX
        try:
            from .okx_ws import OkxWSCollector
            # OKX cần instId dạng BTC-USDT
            okx_symbols = [s.replace("USDT","-USDT") if "-" not in s else s for s in self.symbols]
            # Hack: OkxWSCollector nhận symbols, nhưng nó sẽ subscribe với instId
            # Tạm dùng BTC-USDT
            c = OkxWSCollector(okx_symbols)
            await c.connect()
            self._active = c
            self._ws = c._ws
            logger.info("Multi: dùng OKX")
            return
        except Exception as e:
            logger.warning(f"OKX fail, fallback Coinbase mock: {e}")
        # Cuối cùng: mock realtime từ REST polling Coinbase/OKX
        self._active = None
        logger.info("Multi: dùng REST polling fallback")

    async def subscribe(self):
        if self._active:
            await self._active.subscribe()

    async def stream(self) -> AsyncIterator[MarketEvent]:
        if self._active:
            async for ev in self._active.stream():
                yield ev
        else:
            # Polling fallback: mỗi 500ms fetch price via REST
            import time
            while True:
                for sym in self.symbols:
                    try:
                        price, src = fetch_price_fallback(sym)
                        payload = {"p": str(price), "q": "0.01", "s": sym, "T": int(time.time()*1000)}
                        # Dùng TradeEvent giả
                        yield TradeEvent(source=src, symbol=sym, price=price, qty=0.01, payload=payload)
                    except Exception as e:
                        yield MarketEvent(source="mock", symbol=sym, payload={"error": str(e)})
                await asyncio.sleep(0.5)

    async def fetch_snapshot(self, symbol: str):
        # Vision snapshot không chặn
        try:
            import requests
            url = f"https://data-api.binance.vision/api/v3/depth?symbol={symbol}&limit=100"
            r = requests.get(url, timeout=5)
            if r.status_code == 200:
                return r.json()
        except Exception:
            pass
        # fallback OKX
        try:
            okx_sym = symbol.replace("USDT","-USDT")
            r = requests.get(f"https://www.okx.com/api/v5/market/books?instId={okx_sym}&sz=20", timeout=5)
            data = r.json()
            if data.get("code")=="0":
                d = data["data"][0]
                return {"lastUpdateId": int(d["ts"]), "bids": d["bids"], "asks": d["asks"]}
        except Exception:
            pass
        # cuối cùng dùng active collector nếu có
        if self._active and hasattr(self._active, 'fetch_snapshot'):
            return await self._active.fetch_snapshot(symbol)
        raise RuntimeError("No snapshot fallback")
