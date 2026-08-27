"""AccountRepository."""
from ...portfolio.virtual_account import VirtualAccount

class AccountRepository:
    def __init__(self):
        self._store: dict[str, VirtualAccount] = {}
    def save(self, acc: VirtualAccount):
        self._store[acc.id] = acc
    def get(self, id: str) -> VirtualAccount | None:
        return self._store.get(id)
    def list_all(self) -> list[VirtualAccount]:
        return list(self._store.values())
