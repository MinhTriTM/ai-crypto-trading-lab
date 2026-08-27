"""Funding features."""
def funding_rate_to_apr(rate: float) -> float:
    return rate * 3 * 365
def funding_signal(rate: float, threshold: float = 0.001) -> str:
    if rate > threshold: return "short_bias"
    if rate < -threshold: return "long_bias"
    return "neutral"
