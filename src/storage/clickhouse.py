"""Clickhouse."""
class Clickhouse:
    def __init__(self, host: str = "localhost", port: int = 9000, database: str = "market_data"):
        self.host = host
        self.port = port
        self.database = database
        self.client = None

    def connect(self):
        try:
            from clickhouse_driver import Client
            self.client = Client(host=self.host, port=self.port, database=self.database)
            print("ClickHouse connected")
        except ImportError:
            print("clickhouse-driver not installed, using mock")
            self.client = "mock"

    def insert_trades(self, trades: list[dict]):
        if self.client == "mock":
            print(f"Mock insert {len(trades)} trades")
            return
        self.client.execute(f"INSERT INTO {self.database}.trades VALUES", trades)

    def query(self, sql: str):
        if self.client == "mock":
            return []
        return self.client.execute(sql)
