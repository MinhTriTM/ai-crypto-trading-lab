"""Delta - cap nhat gia tang."""
from dataclasses import dataclass, field
from typing import List, Tuple

@dataclass
class Delta:
    symbol: str
    bids: List[Tuple[float,float]]
    asks: List[Tuple[float,float]]
    first_update_id: int = 0
    final_update_id: int = 0
    timestamp: int = 0

    def is_valid(self, last_update_id: int) -> bool:
        return self.first_update_id <= last_update_id + 1 <= self.final_update_id
