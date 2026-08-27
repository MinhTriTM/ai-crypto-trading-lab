"""EpisodeRunner - chay 1 episode."""
from .environment import TradingEnv
from .episode import Episode
from src.ai.agent.trading_agent import TradingAgent

class EpisodeRunner:
    def __init__(self, env: TradingEnv, agent: TradingAgent):
        self.env = env
        self.agent = agent

    def run(self, max_steps: int = 1000) -> Episode:
        obs, _ = self.env.reset()
        ep = Episode(start_equity=self.env.account.equity)
        done = False
        while not done and len(ep.steps) < max_steps:
            action = self.agent.decide(obs)
            obs, reward, done, truncated, info = self.env.step(action)
            ep.add_step(obs, action, reward, info["equity"])
            if truncated:
                ep.done_reason = "truncated"
                break
            if done:
                ep.done_reason = "bankrupt" if self.env.account.is_bankrupt else "target"
        ep.end_equity = self.env.account.equity
        return ep
