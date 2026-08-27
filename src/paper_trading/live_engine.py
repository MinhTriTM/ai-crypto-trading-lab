"""LiveEngine - vong lap realtime."""
import asyncio
from src.market.collectors.binance_ws import BinanceWSCollector
from src.ai.agent.trading_agent import TradingAgent
from src.portfolio.virtual_account import VirtualAccount
from src.exchange_simulator.virtual_exchange import VirtualExchange
from src.utils.logger import get_logger
logger = get_logger('paper.live')

class LiveEngine:
    def __init__(self, symbols: list[str] = ["BTCUSDT"], agent: TradingAgent | None = None):
        self.symbols = symbols
        self.agent = agent or TradingAgent()
        self.accounts: list[VirtualAccount] = [VirtualAccount(initial_balance=1000, target=10000)]
        self.exchange = VirtualExchange()
        self.collector = BinanceWSCollector(symbols)
        self._running = False

    async def start(self):
        self._running = True
        logger.info(f"Live paper trading bat dau symbols={self.symbols}")
        # tao task collector
        async for event in self.collector.start():
            if not self._running:
                break
            await self.on_market_event(event)

    async def on_market_event(self, event):
        # update orderbook price
        price = getattr(event, 'price', 67000)
        # moi account ra quyet dinh
        for acc in self.accounts:
            state = self.agent.observe({"features": [price]}, {"vector": [acc.equity/10000,0,0,0,0,0], "goal": [0,0,0,0]})
            action = self.agent.decide(state)
            order = action.to_order(acc.equity, price)
            if order:
                trades = self.exchange.place_order(order)
                for t in trades:
                    acc.apply_trade(t)
                logger.info(f"Account {acc.id} {action} equity={acc.equity:.2f} trades={len(trades)}")

    def stop(self):
        self._running = False
        logger.info("Live engine stopped")

    def get_performance(self) -> dict:
        return {acc.id: acc.to_dict() for acc in self.accounts}
