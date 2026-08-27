"""Redis."""
try:
    import redis.asyncio as aioredis
except ImportError:
    aioredis = None

class Redis:
    def __init__(self, host: str = "localhost", port: int = 6379, db: int = 0):
        self.host = host
        self.port = port
        self.db = db
        self.client = None

    async def connect(self):
        if aioredis:
            self.client = aioredis.Redis(host=self.host, port=self.port, db=self.db, decode_responses=True)
            await self.client.ping()
            print("Redis connected")
        else:
            self.client = {}
            print("Redis mock")

    async def set(self, key: str, value: str, ex: int | None = None):
        if isinstance(self.client, dict):
            self.client[key] = value
        else:
            await self.client.set(key, value, ex=ex)

    async def get(self, key: str):
        if isinstance(self.client, dict):
            return self.client.get(key)
        return await self.client.get(key)

    async def publish(self, channel: str, message: str):
        if isinstance(self.client, dict):
            print(f"Mock publish {channel}: {message}")
        else:
            await self.client.publish(channel, message)
