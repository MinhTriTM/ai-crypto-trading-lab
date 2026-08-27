"""RewardEngine - tong hop reward."""
from .profit_reward import profit_reward
from .risk_penalty import risk_penalty
from .drawdown_penalty import drawdown_penalty
from .target_reward import target_reward

class RewardEngine:
    def __init__(self, w_profit: float = 1.0, w_risk: float = 0.5, w_dd: float = 0.5, w_target: float = 2.0):
        self.w_profit = w_profit
        self.w_risk = w_risk
        self.w_dd = w_dd
        self.w_target = w_target

    def calculate(self, prev_equity: float, curr_equity: float, drawdown: float, is_target: bool, is_bankrupt: bool) -> float:
        r = 0.0
        r += self.w_profit * profit_reward(prev_equity, curr_equity)
        r -= self.w_risk * risk_penalty(curr_equity, prev_equity)
        r -= self.w_dd * drawdown_penalty(drawdown)
        r += self.w_target * target_reward(is_target, is_bankrupt)
        # clip
        return max(-10, min(10, r))
