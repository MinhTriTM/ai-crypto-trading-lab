"""NearestNeighbors - tim K trang thai lich su gan nhat."""
import numpy as np
from typing import List, Tuple

class NearestNeighbors:
    def __init__(self, k: int = 10):
        self.k = k
        self.vectors: np.ndarray | None = None
        self.metas: list = []

    def build(self, vectors: np.ndarray, metas: list):
        self.vectors = vectors
        self.metas = metas

    def query(self, q: np.ndarray, k: int | None = None) -> List[Tuple[int, float, dict]]:
        k = k or self.k
        if self.vectors is None:
            return []
        # cosine similarity
        sims = self.vectors @ q / (np.linalg.norm(self.vectors, axis=1) * np.linalg.norm(q) + 1e-9)
        idx = np.argsort(sims)[::-1][:k]
        return [(int(i), float(sims[i]), self.metas[i]) for i in idx]
