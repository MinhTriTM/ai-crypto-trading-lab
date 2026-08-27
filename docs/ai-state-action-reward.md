# AI State/Action/Reward

## State (48 dim)
- market 32: features tu FeatureEngine
- portfolio 6: equity, free, exposure, unrealized, drawdown, leverage
- goal 4: progress, current/target, steps, bias

## Action
- Hold, Long, Short, PositionTarget
- Chuyen thanh Order: qty = equity * size_pct * leverage / price

## Reward
- profit_reward: return *100
- risk_penalty: neu volatility cao
- drawdown_penalty: dd >5% bi phat
- target_reward: +10 neu dat target, -10 neu pha san
- Tong: clamp [-10,10]
