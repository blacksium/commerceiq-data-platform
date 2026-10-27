CREATE TABLE IF NOT EXISTS raw.load_batches (
    batch_id UUID PRIMARY KEY,
    source_name TEXT NOT NULL,
    source_file TEXT NOT NULL,
    file_sha256 TEXT NOT NULL,
    row_count BIGINT NOT NULL,
    loaded_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,

    UNIQUE (source_name, file_sha256),
    CHECK (row_count >= 0)
);
