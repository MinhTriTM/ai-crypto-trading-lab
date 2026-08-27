"""StateBuilder - gop market + portfolio + goal thanh vector."""
import numpy as np
from .market_state import MarketState
from .portfolio_state import PortfolioState
from .goal_state import GoalState

class StateBuilder:
    def __init__(self, market_dim: int = 32, portfolio_dim: int = 6, goal_dim: int = 4):
        self.market_dim = market_dim

    def build(self, market_data: dict, portfolio_data: dict) -> np.ndarray:
        # market_data: {price, features, imbalance...}
        # portfolio_data: {equity, exposure...}
        m_feat = market_data.get("features", np.zeros(32))
        if isinstance(m_feat, list):
            m_feat = np.array(m_feat, dtype=np.float32)
        p_vec = portfolio_data.get("vector", [1,1,0,0,0,0.2])
        g_vec = portfolio_data.get("goal", [0,0,0,0])
        state = np.concatenate([m_feat[:32], np.array(p_vec, dtype=np.float32), np.array(g_vec, dtype=np.float32)])
        # pad to 48
        if len(state) < 48:
            state = np.pad(state, (0, 48-len(state)))
        return state[:48].astype(np.float32)

    def build_from_objects(self, ms: MarketState, ps: PortfolioState, gs: GoalState) -> np.ndarray:
        return self.build({"features": ms.features}, {"vector": ps.to_vector(), "goal": [gs.progress, gs.current/gs.target, gs.steps/gs.max_steps, 1.0]})
