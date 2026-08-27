# Branching Engine

## Branch
```
Branch #8F82A1
Parent: #172918
Market: BTCUSDT
Action: LONG 17% x2
Decision offset: +7ms
Data latency: 4.3ms
Order latency: 8.1ms
Target: 10,000 USDT
```

## Dimensions (8)
- asset, direction, position_size, leverage, time_offset, latency, exit_time, market_scenario

## Generation
- Generate N branch tu cung market state
- Expand: HOLD, CLOSE 25%/100%, ADD 5%/20%, REVERSE, WAIT 10ms

## Pruning
- Scorer: ret*10 + progress*5
- Pruner: giu 30% tot nhat
- DiversityFilter: gioi han moi asset/direction

## Population
- Selection: tournament, roulette, top_k
- Mutation, Crossover, Novelty search
