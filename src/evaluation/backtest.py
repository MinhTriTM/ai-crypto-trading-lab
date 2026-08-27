"""Backtest."""
from typing import List
from src.simulation.episode import Episode

class Backtest:
    def run(self, env_fn, agent_fn, n_episodes: int = 100) -> List[Episode]:
        from src.simulation.episode_runner import EpisodeRunner
        episodes = []
        for _ in range(n_episodes):
            env = env_fn()
            agent = agent_fn()
            runner = EpisodeRunner(env, agent)
            episodes.append(runner.run())
        return episodes

    def walk_forward(self, data_splits: list, env_fn, agent_fn):
        # placeholder
        results = []
        for split in data_splits:
            eps = self.run(env_fn, agent_fn, n_episodes=10)
            results.append(eps)
        return results
