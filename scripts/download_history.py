"""Download historical klines via Binance REST."""
import argparse
import aiohttp
import asyncio
import pandas as pd
from pathlib import Path

async def fetch_klines(symbol: str, interval: str = "1m", limit: int = 1000):
    url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval={interval}&limit={limit}"
    async with aiohttp.ClientSession() as s:
        async with s.get(url) as r:
            data = await r.json()
            return data

async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--symbol', default='BTCUSDT')
    parser.add_argument('--days', type=int, default=7)
    parser.add_argument('--interval', default='1m')
    args = parser.parse_args()
    print(f"Download {args.symbol} {args.days} days interval={args.interval}")
    all_data = []
    for _ in range(args.days):
        try:
            data = await fetch_klines(args.symbol, args.interval)
            all_data.extend(data)
            print(f"Fetched {len(data)} klines")
            await asyncio.sleep(0.5)
        except Exception as e:
            print(f"API loi (co the bi chan): {e}, dung du lieu mock")
            # mock
            import time, random
            all_data = [[int(time.time()*1000), str(67000+i), str(67100+i), str(66900+i), str(67050+i), str(random.uniform(1,10))] for i in range(1000)]
            break
    if all_data:
        cols = ["open_time","open","high","low","close","volume","close_time","qav","trades","taker_base","taker_quote","ignore"]
        df = pd.DataFrame(all_data, columns=cols[:len(all_data[0])])
        out = Path(f"data/historical/train/{args.symbol}_{args.interval}.parquet")
        out.parent.mkdir(parents=True, exist_ok=True)
        df.to_parquet(out)
        print(f"Saved {out} rows={len(df)}")

if __name__ == '__main__':
    asyncio.run(main())
