"""Evaluate."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import argparse
from pathlib import Path
from src.evaluation.evaluator import Evaluator
from src.evaluation.backtest import Backtest
from src.simulation.environment import TradingEnv
from src.ai.agent.trading_agent import TradingAgent

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--run', default='runs/training/latest')
    parser.add_argument('--episodes', type=int, default=50)
    args = parser.parse_args()
    print(f"Evaluate run={args.run} episodes={args.episodes}")
    bt = Backtest()
    episodes = bt.run(lambda: TradingEnv(), lambda: TradingAgent(), n_episodes=args.episodes)
    ev = Evaluator()
    result = ev.evaluate(episodes)
    print("Ket qua:", result)
    # luu
    out = Path(args.run) / "eval.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    import json
    out.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding='utf-8')
    print(f"Saved {out}")

if __name__ == '__main__':
    main()
