# Virtual Exchange

Mo phong san that:
- Matching: market/limit, partial_fill, price-time priority
- Execution: effective_price = mid +/- spread/2 +/- slippage
- Latency: gauss(mean=8.1ms, jitter=2ms)
- Slippage: base 5bps + volume_impact
- Fees: maker 0.02%, taker 0.04%, funding 8h
- Derivatives: leverage 1-10x, maintenance 0.5%, liquidation
