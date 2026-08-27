CREATE TABLE IF NOT EXISTS accounts (
    id VARCHAR(20) PRIMARY KEY,
    initial_balance DOUBLE PRECISION NOT NULL,
    target DOUBLE PRECISION NOT NULL,
    created_at BIGINT NOT NULL,
    status VARCHAR(20) DEFAULT 'active'
);

CREATE TABLE IF NOT EXISTS balances (
    account_id VARCHAR(20) REFERENCES accounts(id),
    currency VARCHAR(10) NOT NULL,
    free DOUBLE PRECISION NOT NULL,
    locked DOUBLE PRECISION NOT NULL,
    PRIMARY KEY (account_id, currency)
);

CREATE TABLE IF NOT EXISTS positions (
    account_id VARCHAR(20) REFERENCES accounts(id),
    symbol VARCHAR(20) NOT NULL,
    side VARCHAR(10) NOT NULL,
    qty DOUBLE PRECISION NOT NULL,
    entry_price DOUBLE PRECISION NOT NULL,
    mark_price DOUBLE PRECISION NOT NULL,
    leverage DOUBLE PRECISION NOT NULL,
    PRIMARY KEY (account_id, symbol)
);
