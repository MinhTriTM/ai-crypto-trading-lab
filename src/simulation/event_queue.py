"""EventQueue - hang doi event theo thoi gian."""
import heapq
from dataclasses import dataclass, field
from typing import Any

@dataclass(order=True)
class QueuedEvent:
    timestamp: int
    priority: int = 0
    event: Any = field(compare=False, default=None)

class EventQueue:
    def __init__(self):
        self._heap: list[QueuedEvent] = []

    def push(self, timestamp: int, event: Any, priority: int = 0):
        heapq.heappush(self._heap, QueuedEvent(timestamp, priority, event))

    def pop(self) -> QueuedEvent | None:
        if not self._heap:
            return None
        return heapq.heappop(self._heap)

    def peek(self) -> QueuedEvent | None:
        return self._heap[0] if self._heap else None

    def __len__(self):
        return len(self._heap)

    def is_empty(self) -> bool:
        return len(self._heap) == 0
