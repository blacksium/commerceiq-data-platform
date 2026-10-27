CREATE TABLE IF NOT EXISTS raw.customers (
    batch_id UUID NOT NULL,
    source_row_number BIGINT NOT NULL,
    source_file TEXT NOT NULL,
    loaded_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,

    customer_id TEXT,
    customer_unique_id TEXT,
    customer_zip_code_prefix TEXT,
    customer_city TEXT,
    customer_state TEXT,

    PRIMARY KEY (batch_id, source_row_number),
    FOREIGN KEY (batch_id)
        REFERENCES raw.load_batches (batch_id),
    CHECK (source_row_number > 0)
);
