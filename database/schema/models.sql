CREATE TABLE IF NOT EXISTS models (
    id VARCHAR(40) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    version VARCHAR(20) NOT NULL,
    algorithm VARCHAR(20) NOT NULL,
    path VARCHAR(500) NOT NULL,
    metrics JSONB,
    created_at BIGINT NOT NULL,
    status VARCHAR(20) DEFAULT 'staging' -- staging | production | archived
);

CREATE TABLE IF NOT EXISTS checkpoints (
    id SERIAL PRIMARY KEY,
    model_id VARCHAR(40) REFERENCES models(id),
    step INT NOT NULL,
    path VARCHAR(500) NOT NULL,
    reward DOUBLE PRECISION,
    created_at BIGINT NOT NULL
);
