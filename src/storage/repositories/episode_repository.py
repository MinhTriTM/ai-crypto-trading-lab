"""EpisodeRepository."""
from ...simulation.episode import Episode

class EpisodeRepository:
    def __init__(self):
        self._episodes: list[Episode] = []
    def save(self, ep: Episode):
        self._episodes.append(ep)
    def list_all(self) -> list[Episode]:
        return self._episodes
    def stats(self) -> dict:
        if not self._episodes: return {}
        rets = [e.return_pct for e in self._episodes]
        return {"count": len(self._episodes), "avg_return": sum(rets)/len(rets), "best": max(rets), "worst": min(rets)}
