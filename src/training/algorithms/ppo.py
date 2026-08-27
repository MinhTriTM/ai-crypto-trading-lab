"""PPO algorithm wrapper."""
from dataclasses import dataclass
try:
    import torch
    import torch.nn as nn
    import torch.optim as optim
    _TORCH = True
except ImportError:
    _TORCH = False
    torch = None

@dataclass
class PPOConfig:
    lr: float = 3e-4
    gamma: float = 0.99
    gae_lambda: float = 0.95
    clip_range: float = 0.2
    n_epochs: int = 10
    batch_size: int = 64
    ent_coef: float = 0.01

class PPO:
    def __init__(self, actor, critic, config: PPOConfig = PPOConfig()):
        self.actor = actor
        self.critic = critic
        self.cfg = config
        if _TORCH:
            self.optimizer = optim.Adam(list(actor.parameters()) + list(critic.parameters()), lr=config.lr)
        else:
            self.optimizer = None
    def update(self, rollout):
        if not _TORCH:
            return {"policy_loss": 0.0, "value_loss": 0.0}
        states = torch.FloatTensor(rollout["states"])
        actions = torch.LongTensor(rollout["actions"])
        returns = torch.FloatTensor(rollout["returns"])
        values = self.critic(states)
        advantages = returns - values.detach()
        probs = self.actor(states)
        log_probs = torch.log(probs.gather(1, actions.unsqueeze(1)).squeeze(1) + 1e-9)
        loss = -(log_probs * advantages).mean() - self.cfg.ent_coef * (-(probs * torch.log(probs+1e-9)).sum(1).mean())
        v_loss = ((values - returns)**2).mean()
        total = loss + 0.5 * v_loss
        self.optimizer.zero_grad()
        total.backward()
        torch.nn.utils.clip_grad_norm_(list(self.actor.parameters())+list(self.critic.parameters()), 0.5)
        self.optimizer.step()
        return {"policy_loss": float(loss), "value_loss": float(v_loss)}
