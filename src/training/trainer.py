"""Trainer - vong lap huan luyen chinh."""
from dataclasses import dataclass
import time
from src.utils.logger import get_logger
logger = get_logger('training')

@dataclass
class TrainerConfig:
    total_timesteps: int = 10_000_000
    save_interval: int = 100_000
    log_interval: int = 1000
    device: str = "cuda"

class Trainer:
    def __init__(self, env, agent, config: TrainerConfig = TrainerConfig()):
        self.env = env
        self.agent = agent
        self.cfg = config
        self.timestep = 0

    def train(self):
        logger.info(f"Bat dau train {self.cfg.total_timesteps} timesteps")
        obs, _ = self.env.reset()
        while self.timestep < self.cfg.total_timesteps:
            action = self.agent.decide(obs)
            order = action.to_order(1000, 67000)
            next_obs, reward, done, truncated, info = self.env.step(action)
            self.timestep += 1
            if self.timestep % self.cfg.log_interval == 0:
                logger.info(f"step {self.timestep} reward={reward:.3f} equity={info.get('equity',0):.2f}")
            if self.timestep % self.cfg.save_interval == 0:
                self.save(f"models/checkpoints/step_{self.timestep}.pt")
            obs = next_obs
            if done or truncated:
                obs, _ = self.env.reset()
        logger.info("Train xong")

    def save(self, path: str):
        import torch
        if hasattr(self.agent, 'policy') and hasattr(self.agent.policy, 'state_dict'):
            torch.save(self.agent.policy.state_dict(), path)
            logger.info(f"Saved {path}")

    def evaluate(self, n_episodes: int = 10) -> dict:
        rets = []
        for _ in range(n_episodes):
            obs, _ = self.env.reset()
            done = False
            total = 0
            while not done:
                action = self.agent.decide(obs)
                obs, reward, done, truncated, info = self.env.step(action)
                total += reward
                if truncated: break
            rets.append(total)
        return {"mean_return": sum(rets)/len(rets), "episodes": n_episodes}
