"""PartialFill - mo phong khop tung phan."""
import random
from dataclasses import dataclass

@dataclass
class PartialFillConfig:
    enabled: bool = True
    min_fill_ratio: float = 0.5
    max_fill_ratio: float = 1.0

def simulate_partial_fill(qty: float, cfg: PartialFillConfig = PartialFillConfig()) -> tuple[float, bool]:
    if not cfg.enabled:
        return qty, True
    ratio = random.uniform(cfg.min_fill_ratio, cfg.max_fill_ratio)
    filled = qty * ratio
    is_full = ratio >= 0.99
    return filled, is_full
