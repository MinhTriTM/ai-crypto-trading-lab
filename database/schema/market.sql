-- Market data schema - ClickHouse style nhung tuong thich Postgres
CREATE TABLE IF NOT EXISTS trades (
    symbol VARCHAR(20) NOT NULL,
    price DOUBLE PRECISION NOT NULL,
    qty DOUBLE PRECISION NOT NULL,
    side VARCHAR(4) NOT NULL,
    timestamp BIGINT NOT NULL,
    exchange VARCHAR(20) NOT NULL,
    PRIMARY KEY (symbol, timestamp)
);
CREATE INDEX IF NOT EXISTS idx_trades_symbol_ts ON trades(symbol, timestamp);

CREATE TABLE IF NOT EXISTS orderbook_snapshots (
    symbol VARCHAR(20) NOT NULL,
    bids JSONB NOT NULL,
    asks JSONB NOT NULL,
    timestamp BIGINT NOT NULL,
    last_update_id BIGINT NOT NULL
);

CREATE TABLE IF NOT EXISTS funding_rates (
    symbol VARCHAR(20) NOT NULL,
    funding_rate DOUBLE PRECISION NOT NULL,
    mark_price DOUBLE PRECISION NOT NULL,
    timestamp BIGINT NOT NULL
);

CREATE TABLE IF NOT EXISTS features (
    symbol VARCHAR(20) NOT NULL,
    timestamp BIGINT NOT NULL,
    features JSONB NOT NULL,
    PRIMARY KEY (symbol, timestamp)
);
