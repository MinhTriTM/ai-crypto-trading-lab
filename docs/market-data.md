# Market Data

## Collector
- Binance WS: `wss://stream.binance.com:9443/ws` - trade, depth, ticker, futures (markPrice, forceOrder)
- Bybit, OKX, Coinbase tuong tu

## Orderbook
- Snapshot + Delta reconstruction
- Luu parquet: `data/raw/binance/spot/BTCUSDT/orderbook/`

## Features
- price, volume, volatility, orderflow, imbalance, funding
- FeatureEngine build vector 32 chieu cho AI

## Clock
- MarketClock: dong ho thi truong, chi tien khong lui
- LatencyClock: mo phong data_latency 4.3ms + order_latency 8.1ms
