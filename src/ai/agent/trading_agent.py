"""TradingAgent - AI chinh ra quyet dinh."""
from dataclasses import dataclass
from typing import Optional
import numpy as np
from ..state.state_builder import StateBuilder
from ..actions.action import Action
from ..reward.reward_engine import RewardEngine

@dataclass
class TradingAgent:
    state_builder: StateBuilder = None
    reward_engine: RewardEngine = None
    policy: object = None  # actor model

    def __post_init__(self):
        if self.state_builder is None:
            from ..state.state_builder import StateBuilder
            self.state_builder = StateBuilder()
        if self.reward_engine is None:
            from ..reward.reward_engine import RewardEngine
            self.reward_engine = RewardEngine()

    def observe(self, market_data: dict, portfolio_state: dict) -> np.ndarray:
        return self.state_builder.build(market_data, portfolio_state)

    def decide(self, state: np.ndarray) -> Action:
        # neu co policy thi dung, khong thi random demo
        if self.policy and hasattr(self.policy, 'predict'):
            idx = self.policy.predict(state)
        else:
            # 0: hold, 1: long, 2: short
            idx = int(np.random.choice([0,1,2], p=[0.6,0.2,0.2]))
        from ..actions.hold import HoldAction
        from ..actions.long import LongAction
        from ..actions.short import ShortAction
        if idx == 1:
            return LongAction(symbol="BTCUSDT", size_pct=0.1, leverage=2)
        elif idx == 2:
            return ShortAction(symbol="BTCUSDT", size_pct=0.1, leverage=2)
        return HoldAction()

    def update(self, reward: float):
        pass
