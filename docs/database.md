# Database

## Postgres (accounts, trades, training, models)
- accounts, balances, positions
- orders, trades, pnl_history
- episodes, experiences, training_runs
- models, checkpoints

## ClickHouse (market_data)
- trades, orderbook_snapshots, funding_rates, features

## Redis (cache/pubsub)
- market tick cache, training progress

## Parquet (processed)
- data/processed/ticks, orderbooks, features, market_states
