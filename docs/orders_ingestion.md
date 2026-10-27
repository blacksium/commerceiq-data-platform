# Raw Orders Ingestion

## Purpose

Load the Olist orders CSV into PostgreSQL while preserving source
values and recording where each record came from.

## Prerequisites

- Activate the project virtual environment.
- Start PostgreSQL with Docker Compose.
- Configure database credentials in the ignored .env file.
- Apply the SQL files in numerical order.
- Keep the source CSV at:
  data/raw/olist/olist_orders_dataset.csv

## Run

    source .venv/bin/activate
    docker compose up -d --wait
    python scripts/load_orders.py

## Design

- raw.orders stores source records and loading metadata.
- Source fields remain text, including timestamps.
- Blank source values remain empty strings.
- Each batch receives a generated UUID.
- Source record numbering starts at 1, excluding the CSV header.
- The raw primary key is (batch_id, source_row_number).
- raw.load_batches records the source filename, SHA256 and row count.
- A unique constraint on (source_name, file_sha256) prevents
  registering the same file contents twice for the same source.
- PostgreSQL COPY loads the order records.
- The batch register and order records share one transaction.
- A changed file fingerprint is treated as a new batch.
- Multiple batches are preserved; downstream queries must choose
  the intended batch rather than count all snapshots together.

## Verified results

- First load: 99,441 records.
- Distinct order IDs: 99,441.
- Stored batches: 1.
- Registered row count matches the stored row count.
- Rerunning the same file skips loading.
- Stored row count remains 99,441 after the rerun.

## Rollback verification

Tested with a temporary CSV containing one order while telling
the loading function to expect two records.

- The loader raised the expected row-count error.
- Before the attempt: 99,441 orders and 1 batch.
- After the attempt: 99,441 orders and 1 batch.
- The transaction rolled back the test order and batch registration.
- The original source CSV was unchanged.
