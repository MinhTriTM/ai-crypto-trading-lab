"""Paper trade realtime."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import asyncio
import argparse
from src.paper_trading.live_engine import LiveEngine

async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--symbol', default='BTCUSDT')
    parser.add_argument('--duration', type=int, default=60)
    args = parser.parse_args()
    print(f"Paper trade {args.symbol} duration={args.duration}s (Ctrl+C de dung)")
    engine = LiveEngine(symbols=[args.symbol])
    try:
        await asyncio.wait_for(engine.start(), timeout=args.duration)
    except asyncio.TimeoutError:
        print("Het thoi gian paper trade")
        engine.stop()
        print(engine.get_performance())
    except KeyboardInterrupt:
        engine.stop()

if __name__ == '__main__':
    asyncio.run(main())
