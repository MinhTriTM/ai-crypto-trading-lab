"""Database - factory."""
from typing import Optional

class Database:
    def __init__(self, dsn: str):
        self.dsn = dsn
        self._engine = None

    async def connect(self):
        # placeholder
        print(f"Connect DB {self.dsn}")
        self._engine = "connected"

    async def disconnect(self):
        self._engine = None

    async def execute(self, query: str, params: dict | None = None):
        return []

def get_database(name: str = "postgres") -> Database:
    import os
    if name == "postgres":
        dsn = os.getenv("POSTGRES_DSN", "postgresql+asyncpg://lab_user:lab_password@localhost:5432/ai_crypto_lab")
    elif name == "clickhouse":
        dsn = "clickhouse://localhost:9000/market_data"
    else:
        dsn = "redis://localhost:6379/0"
    return Database(dsn)
