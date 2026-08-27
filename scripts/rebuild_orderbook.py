"""Rebuild orderbook tu trades + snapshots."""
import argparse
from src.market.orderbook.reconstruction import OrderBookReconstructor
from src.market.orderbook.snapshot import Snapshot

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--symbol', default='BTCUSDT')
    parser.add_argument('--input', default='data/raw/binance/spot/BTCUSDT/orderbook')
    args = parser.parse_args()
    print(f"Rebuild orderbook {args.symbol} tu {args.input}")
    recon = OrderBookReconstructor(args.symbol)
    snap = Snapshot(symbol=args.symbol, bids=[(67000,1),(66999,2)], asks=[(67001,1),(67002,2)], last_update_id=1)
    recon.init_snapshot(snap)
    print(f"Orderbook mid={recon.book.mid_price} spread={recon.book.spread}")

if __name__ == '__main__':
    main()
