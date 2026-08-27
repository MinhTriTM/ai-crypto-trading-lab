"""Postgres."""
import asyncpg
from typing import Optional

class Postgres:
    def __init__(self, dsn: str = "postgresql://lab_user:lab_password@localhost:5432/ai_crypto_lab"):
        self.dsn = dsn
        self.pool: Optional[asyncpg.Pool] = None

    async def connect(self):
        self.pool = await asyncpg.create_pool(self.dsn)
        print("Postgres connected")

    async def fetch(self, query: str, *args):
        async with self.pool.acquire() as conn:
            return await conn.fetch(query, *args)

    async def execute(self, query: str, *args):
        async with self.pool.acquire() as conn:
            return await conn.execute(query, *args)

    async def close(self):
        if self.pool:
            await self.pool.close()
