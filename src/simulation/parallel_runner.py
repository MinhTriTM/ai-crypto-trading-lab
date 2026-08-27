"""ParallelRunner - chay nhieu episode song song."""
import concurrent.futures
from .episode_runner import EpisodeRunner
from .environment import TradingEnv
from src.ai.agent.trading_agent import TradingAgent

class ParallelRunner:
    def __init__(self, n_workers: int = 8):
        self.n_workers = n_workers

    def run(self, n_episodes: int, env_fn, agent_fn) -> list:
        episodes = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.n_workers) as ex:
            futures = []
            for _ in range(n_episodes):
                env = env_fn()
                agent = agent_fn()
                runner = EpisodeRunner(env, agent)
                futures.append(ex.submit(runner.run))
            for f in concurrent.futures.as_completed(futures):
                episodes.append(f.result())
        return episodes

    def run_vector(self, n_episodes: int, env_fn, agent_fn):
        # placeholder for vector env
        return self.run(n_episodes, env_fn, agent_fn)
