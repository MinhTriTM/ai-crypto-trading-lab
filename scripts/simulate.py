"""Simulate - chay nhieu episode."""
import argparse
from src.simulation.environment import TradingEnv
from src.simulation.parallel_runner import ParallelRunner
from src.ai.agent.trading_agent import TradingAgent

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--episodes', type=int, default=100)
    parser.add_argument('--workers', type=int, default=4)
    args = parser.parse_args()
    print(f"Simulate {args.episodes} episodes workers={args.workers}")
    runner = ParallelRunner(n_workers=args.workers)
    episodes = runner.run(args.episodes, lambda: TradingEnv(), lambda: TradingAgent())
    avg = sum(e.return_pct for e in episodes)/len(episodes) if episodes else 0
    print(f"Xong avg_return={avg:.3%} episodes={len(episodes)}")
    for e in episodes[:3]:
        print(e.to_dict())

if __name__ == '__main__':
    main()
