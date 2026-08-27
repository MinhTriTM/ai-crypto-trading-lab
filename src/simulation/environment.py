"""Environment - Gym-like cho trading."""
import numpy as np
try:
    import gymnasium as gym
    from gymnasium import spaces
    _GYM_AVAILABLE = True
except ImportError:
    _GYM_AVAILABLE = False
    gym = object
    spaces = None
from src.portfolio.virtual_account import VirtualAccount
from src.exchange_simulator.virtual_exchange import VirtualExchange
from src.ai.state.state_builder import StateBuilder

class TradingEnv(gym.Env if _GYM_AVAILABLE else object):
    """Moi truong giao dich cho RL."""
    def __init__(self, exchange: VirtualExchange | None = None, initial_balance: float = 1000.0):
        if _GYM_AVAILABLE:
            super().__init__()
        self.exchange = exchange or VirtualExchange()
        self.initial_balance = initial_balance
        self.account = VirtualAccount(initial_balance=initial_balance)
        self.builder = StateBuilder()
        if _GYM_AVAILABLE:
            self.observation_space = spaces.Box(low=-10, high=10, shape=(48,), dtype=np.float32)
            self.action_space = spaces.Discrete(3)  # hold, long, short
        self.current_price = 67000.0
        self.step_count = 0
        self.max_steps = 1000

    def reset(self, seed=None, options=None):
        if _GYM_AVAILABLE:
            super().reset(seed=seed)
        self.account = VirtualAccount(initial_balance=self.initial_balance)
        self.step_count = 0
        self.current_price = 67000.0 + np.random.randn()*100
        obs = self._get_obs()
        return obs, {}

    def step(self, action):
        # action: int hoac Action object
        if isinstance(action, int):
            from src.ai.actions.hold import HoldAction
            from src.ai.actions.long import LongAction
            from src.ai.actions.short import ShortAction
            mapping = {0: HoldAction(), 1: LongAction(size_pct=0.1, leverage=2), 2: ShortAction(size_pct=0.1, leverage=2)}
            action = mapping.get(action, HoldAction())
        # thuc hien
        prev_equity = self.account.equity
        order = action.to_order(self.account.equity, self.current_price)
        if order:
            trades = self.exchange.place_order(order)
            for t in trades:
                self.account.apply_trade(t)
        # gia ngau nhien walk
        self.current_price += np.random.randn()*10
        self.current_price = max(1000, self.current_price)
        self.step_count += 1
        obs = self._get_obs()
        reward = (self.account.equity - prev_equity) / prev_equity * 100 if prev_equity else 0
        done = self.account.is_bankrupt or self.account.is_target_reached
        truncated = self.step_count >= self.max_steps
        info = {"equity": self.account.equity, "price": self.current_price}
        return obs, reward, done, truncated, info

    def _get_obs(self):
        market_data = {"features": np.random.randn(32).astype(np.float32)}
        portfolio_data = {"vector": [self.account.equity/10000, 0,0,0,0,0], "goal": [0,0,0,0]}
        return self.builder.build(market_data, portfolio_data)
