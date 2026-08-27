# Training

## Algorithms
- PPO (chinh), SAC, TD3, Evolutionary

## Experience
- ReplayBuffer 1M, RolloutBuffer 2048, Sampler uniform/prioritized

## Curriculum
- easy (sideways, 0.3) -> medium (mixed, 0.6) -> hard (volatile, 1.0)

## Distributed
- VectorEnv 32 env song song
- DistributedTrainer 4 workers

## Simulation
- TradingEnv (Gym), Episode, ParallelRunner, Scenario (bull/bear/flash_crash)

## Evaluation
- Sharpe, MaxDrawdown, WinRate, SurvivalRate, TargetSuccessRate
- WalkForward, StressTest, Robustness (latency/slippage)
