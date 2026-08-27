"""Confidence."""
import numpy as np

def confidence_by_sample_size(n: int, min_n: int = 30) -> float:
    if n < 5:
        return 0.1
    return min(1.0, n / (min_n * 2) + 0.5)

def confidence_by_std(std: float) -> float:
    # std cang nho -> confidence cao
    return float(1 / (1 + std*10))

def combined_confidence(n: int, std: float) -> float:
    return confidence_by_sample_size(n) * confidence_by_std(std)
