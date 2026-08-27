"""PerformanceTracker - theo doi hieu suat paper."""
from dataclasses import dataclass, field
import time

@dataclass
class PerformanceTracker:
    equities: list[float] = field(default_factory=list)
    timestamps: list[int] = field(default_factory=list)
    trades: list[dict] = field(default_factory=list)

    def update(self, equity: float, timestamp: int | None = None):
        self.equities.append(equity)
        self.timestamps.append(timestamp or int(time.time()*1000))

    def add_trade(self, trade: dict):
        self.trades.append(trade)

    def stats(self) -> dict:
        if not self.equities:
            return {}
        start = self.equities[0]
        end = self.equities[-1]
        peak = max(self.equities)
        dd = (peak - end)/peak if peak else 0
        total_ret = (end-start)/start if start else 0
        return {"start": start, "end": end, "return": total_ret, "max_drawdown": dd, "trades": len(self.trades), "peak": peak}

    def is_healthy(self) -> bool:
        s = self.stats()
        return s.get("max_drawdown", 0) < 0.15 and s.get("return", 0) > -0.1
