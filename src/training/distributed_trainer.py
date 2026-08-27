"""DistributedTrainer."""
from dataclasses import dataclass
import multiprocessing as mp
from .trainer import Trainer, TrainerConfig

@dataclass
class DistributedConfig:
    num_workers: int = 4
    backend: str = "mp"  # mp | ray

class DistributedTrainer:
    def __init__(self, env_fn, agent_fn, config: DistributedConfig = DistributedConfig()):
        self.env_fn = env_fn
        self.agent_fn = agent_fn
        self.cfg = config

    def train(self, total_timesteps: int = 1_000_000):
        per_worker = total_timesteps // self.cfg.num_workers
        # don gian: chay tuan tu, thuc te dung Ray
        results = []
        for i in range(self.cfg.num_workers):
            print(f"[Distributed] worker {i} train {per_worker} steps")
            env = self.env_fn()
            agent = self.agent_fn()
            trainer = Trainer(env, agent, TrainerConfig(total_timesteps=per_worker))
            trainer.train()
            results.append(trainer.timestep)
        return results
