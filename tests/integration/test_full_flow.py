"""Integration: market -> branch -> simulation -> training."""
from src.market.orderbook.orderbook import OrderBook
from src.branching.branch_generator import BranchGenerator
from src.branching.branch_executor import BranchExecutor
from src.exchange_simulator.virtual_exchange import VirtualExchange
from src.simulation.environment import TradingEnv
from src.ai.agent.trading_agent import TradingAgent

def test_full_flow():
    # 1. market
    ob = OrderBook(symbol="BTCUSDT")
    ob.apply_snapshot([(67000,5)], [(67001,5)], 1)
    # 2. branching
    gen = BranchGenerator()
    branches = gen.generate(max_branches=5)
    ex = VirtualExchange()
    ex.update_orderbook(ob)
    executor = BranchExecutor(ex)
    states = executor.execute_batch(branches, ob.mid_price)
    assert len(states) == 5
    # 3. simulation
    env = TradingEnv(exchange=ex)
    agent = TradingAgent()
    obs, _ = env.reset()
    obs, reward, done, truncated, info = env.step(agent.decide(obs))
    assert info["equity"] > 0
