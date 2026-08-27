"""VectorIndex - FAISS wrapper."""
import numpy as np

class VectorIndex:
    """Wrapper cho FAISS, fallback numpy neu khong co."""
    def __init__(self, dim: int = 32):
        self.dim = dim
        self.index = None
        self.metas = []
        try:
            import faiss
            self.faiss = faiss
            self.index = faiss.IndexFlatIP(dim)
            self.use_faiss = True
        except ImportError:
            self.use_faiss = False
            self.vectors = []

    def add(self, vectors: np.ndarray, metas: list):
        if self.use_faiss:
            # normalize for IP = cosine
            import numpy as np
            faiss.normalize_L2(vectors)
            self.index.add(vectors.astype(np.float32))
        else:
            self.vectors.extend(vectors)
        self.metas.extend(metas)

    def search(self, q: np.ndarray, k: int = 10):
        if self.use_faiss:
            import faiss
            q = q.reshape(1,-1).astype(np.float32)
            faiss.normalize_L2(q)
            scores, idxs = self.index.search(q, k)
            return [(int(idxs[0][i]), float(scores[0][i]), self.metas[idxs[0][i]] if idxs[0][i] < len(self.metas) else {}) for i in range(k)]
        else:
            # brute force
            sims = [float(np.dot(v, q) / (np.linalg.norm(v)*np.linalg.norm(q)+1e-9)) for v in self.vectors]
            order = np.argsort(sims)[::-1][:k]
            return [(int(i), float(sims[i]), self.metas[i]) for i in order]
