"""Create dataset - tao features parquet tu raw."""
import argparse
from pathlib import Path
import pandas as pd
import numpy as np
from src.market.features.feature_engine import FeatureEngine
from src.market.orderbook.orderbook import OrderBook

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', default='data/historical/train')
    parser.add_argument('--output', default='data/processed/features')
    args = parser.parse_args()
    print(f"Tao dataset tu {args.input} -> {args.output}")
    Path(args.output).mkdir(parents=True, exist_ok=True)
    engine = FeatureEngine()
    # mock tao 1000 mau
    for i in range(1000):
        price = 67000 + np.random.randn()*100
        engine.update(price, 1.0, OrderBook(symbol="BTCUSDT"))
    feats = engine.build()
    df = pd.DataFrame([feats], columns=[f"f{i}" for i in range(32)])
    out = Path(args.output) / "features.parquet"
    df.to_parquet(out)
    print(f"Saved {out} shape={df.shape}")

if __name__ == '__main__':
    main()
