"""VectorEnv - nhieu env song song."""
import numpy as np
from typing import Callable

class VectorEnv:
    def __init__(self, env_fns: list[Callable]):
        self.envs = [fn() for fn in env_fns]
        self.num_envs = len(self.envs)

    def reset(self):
        obs = [env.reset()[0] for env in self.envs]
        return np.stack(obs), {}

    def step(self, actions):
        results = [env.step(a) for env, a in zip(self.envs, actions)]
        obs = np.stack([r[0] for r in results])
        rewards = np.array([r[1] for r in results])
        dones = np.array([r[2] for r in results])
        truncated = np.array([r[3] for r in results])
        infos = [r[4] for r in results]
        return obs, rewards, dones, truncated, infos

    def close(self):
        for env in self.envs:
            if hasattr(env, 'close'):
                env.close()
