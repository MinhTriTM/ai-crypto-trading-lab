CREATE TABLE IF NOT EXISTS episodes (
    id VARCHAR(40) PRIMARY KEY,
    account_id VARCHAR(20),
    start_equity DOUBLE PRECISION NOT NULL,
    end_equity DOUBLE PRECISION NOT NULL,
    steps INT NOT NULL,
    return_pct DOUBLE PRECISION NOT NULL,
    done_reason VARCHAR(20),
    created_at BIGINT NOT NULL
);

CREATE TABLE IF NOT EXISTS experiences (
    id SERIAL PRIMARY KEY,
    episode_id VARCHAR(40) REFERENCES episodes(id),
    state JSONB NOT NULL,
    action INT NOT NULL,
    reward DOUBLE PRECISION NOT NULL,
    next_state JSONB NOT NULL,
    done BOOLEAN NOT NULL
);

CREATE TABLE IF NOT EXISTS training_runs (
    id VARCHAR(40) PRIMARY KEY,
    algorithm VARCHAR(20) NOT NULL,
    config JSONB NOT NULL,
    start_at BIGINT NOT NULL,
    end_at BIGINT,
    status VARCHAR(20) DEFAULT 'running',
    metrics JSONB
);
