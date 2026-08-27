"""Experience - mot transition."""
from dataclasses import dataclass
import numpy as np

@dataclass
class Experience:
    state: np.ndarray
    action: int
    reward: float
    next_state: np.ndarray
    done: bool
    info: dict = None

    def __post_init__(self):
        if self.info is None:
            self.info = {}
