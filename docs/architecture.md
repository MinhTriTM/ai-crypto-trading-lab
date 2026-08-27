# Architecture

## Tong quan
```
REAL EXCHANGES -> MARKET ENGINE -> AI BRAIN -> VIRTUAL ACCOUNTS -> VIRTUAL EXCHANGE -> EXPERIENCE -> TRAINING
```

## Cac lop
- `src/market`: collectors (Binance/Bybit/OKX/Coinbase), events, orderbook, features, clock
- `src/replay`: historical replay, event replay, replay clock
- `src/exchange_simulator`: virtual_exchange, matching, execution (latency/slippage/spread), fees, derivatives
- `src/portfolio`: virtual_account, wallet, position, order, trade, pnl
- `src/risk`: risk_engine, position_sizing, drawdown, leverage, bankruptcy
- `src/ai`: agent, state (market/portfolio/goal), actions, reward, models (actor/critic/transformer)
- `src/historical_intelligence`: similarity (encoder, nearest_neighbors, vector_index), statistics, pattern_memory
- `src/branching`: branch, dimensions (8 chieu), pruning, population (evolution)
- `src/training`: trainer, distributed, vector_env, algorithms (PPO/SAC/TD3/Evo), experience, curriculum
- `src/simulation`: environment (Gym), episode, parallel_runner, scenario, event_queue
- `src/evaluation`: evaluator, backtest, walk_forward, stress_test, robustness, metrics
- `src/paper_trading`: live_engine, live_account
- `src/storage`: postgres, clickhouse, redis, parquet, repositories
- `src/api`: FastAPI + WebSocket
- `src/utils`: logger, math, time, ids, serialization

## Nguyen tac
- Market data la that, khong fake chart
- Tien ao hoan toan trong RAM/DB, khong lien ket san that
- Enforce no-lookahead bang MarketClock
- Historical replay de train nhanh, live paper de kiem nghiem
