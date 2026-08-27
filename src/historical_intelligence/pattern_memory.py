"""PatternMemory - bo nho pattern lich su."""
from dataclasses import dataclass, field
import numpy as np
from .similarity.state_encoder import StateEncoder
from .similarity.vector_index import VectorIndex
from .statistics.future_returns import conditional_returns

@dataclass
class PatternMemory:
    dim: int = 32
    encoder: StateEncoder = field(default_factory=StateEncoder)
    index: VectorIndex = field(default_factory=VectorIndex)

    def __post_init__(self):
        if isinstance(self.encoder, StateEncoder) and self.encoder.dim != self.dim:
            self.encoder = StateEncoder(dim=self.dim)
        if isinstance(self.index, VectorIndex) and self.index.dim != self.dim:
            self.index = VectorIndex(dim=self.dim)

    def add_history(self, states: list[np.ndarray], future_returns: list[float], metas: list[dict] | None = None):
        vecs = np.stack([self.encoder.encode(s) for s in states])
        if metas is None:
            metas = [{"future_return": r} for r in future_returns]
        else:
            for m, r in zip(metas, future_returns):
                m["future_return"] = r
        self.index.add(vecs.astype(np.float32), metas)

    def query(self, state: np.ndarray, k: int = 20) -> dict:
        q = self.encoder.encode(state)
        neighbors = self.index.search(q, k)
        rets = [m.get("future_return",0) for _,_,m in neighbors]
        stats = conditional_returns(rets) if rets else {"mean":0,"std":0,"p_positive":0.5,"n":0}
        return {"neighbors": neighbors, "stats": stats, "signal": "long" if stats["mean"]>0.001 else "short" if stats["mean"]<-0.001 else "hold"}
