"""StateEncoder - ma hoa market state thanh vector."""
import numpy as np

class StateEncoder:
    def __init__(self, dim: int = 32):
        self.dim = dim
        # random projection demo; thuc te dung transformer
        self.proj = np.random.randn(48, dim) * 0.1

    def encode(self, state: np.ndarray) -> np.ndarray:
        if len(state) < 48:
            state = np.pad(state, (0, 48-len(state)))
        vec = state[:48] @ self.proj
        # L2 normalize
        n = np.linalg.norm(vec)
        return vec / n if n else vec

    def batch_encode(self, states: list[np.ndarray]) -> np.ndarray:
        return np.stack([self.encode(s) for s in states])
