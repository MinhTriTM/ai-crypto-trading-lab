"""Collect market data - chay collector va luu parquet."""
import asyncio
import argparse
from pathlib import Path
from src.market.collectors.binance_ws import BinanceWSCollector
from src.storage.parquet import ParquetStore
import pyarrow as pa

async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--symbol', default='BTCUSDT')
    parser.add_argument('--duration', type=int, default=60, help='giay')
    args = parser.parse_args()
    print(f"[Collect] {args.symbol} trong {args.duration}s")
    collector = BinanceWSCollector([args.symbol])
    store = ParquetStore()
    trades = []
    try:
        # demo mock neu khong co WS
        import random, time
        for i in range(20):
            trades.append({"symbol": args.symbol, "price": 67000+random.uniform(-100,100), "qty": random.uniform(0.01,0.5), "timestamp": int(time.time()*1000)})
            await asyncio.sleep(0.1)
        print(f"Collected {len(trades)} trades")
        if trades:
            import pandas as pd
            df = pd.DataFrame(trades)
            store.append(df, f"ticks/{args.symbol}/{int(time.time())}.parquet")
    except Exception as e:
        print(f"Loi collect: {e}")

if __name__ == '__main__':
    asyncio.run(main())
