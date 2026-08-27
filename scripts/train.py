"""Train."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import argparse
import yaml
from src.simulation.environment import TradingEnv
from src.ai.agent.trading_agent import TradingAgent
from src.training.trainer import Trainer, TrainerConfig

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', default='config/training.yaml')
    parser.add_argument('--timesteps', type=int, default=None)
    args = parser.parse_args()
    with open(args.config, encoding='utf-8') as f:
        cfg = yaml.safe_load(f)
    print(f"Train config: {cfg['training']}")
    env = TradingEnv()
    agent = TradingAgent()
    tcfg = TrainerConfig(total_timesteps=args.timesteps or cfg['training']['total_timesteps'])
    trainer = Trainer(env, agent, tcfg)
    trainer.train()
    print("Train xong, evaluate...")
    print(trainer.evaluate(n_episodes=5))

if __name__ == '__main__':
    main()
