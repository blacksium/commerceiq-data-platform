# Raw Customers Ingestion

## Purpose

Load the Olist customers CSV into raw.customers, preserving
source values and recording batch metadata.

## Run

Apply sql/003_create_raw_customers.sql after SQL files 001 and 002.
With the virtual environment active and PostgreSQL running:

    python scripts/load_customers.py

## Design

- Source columns remain text, including ZIP code prefixes.
- customer_id links customer records to orders.
- customer_unique_id identifies customers across repeat orders.
- The raw primary key is (batch_id, source_row_number).
- A foreign key requires each batch_id to exist in raw.load_batches.
- File fingerprints prevent duplicate loads.
- Customer records and batch registration share one transaction.

## Verified results

- Stored records: 99,441.
- Distinct customer_id values: 99,441.
- Distinct customer_unique_id values: 96,096.
- Customer batches: 1.
- Rerunning the same file skips loading.
- Orders without a matching customer_id: 0.

The relationship check covers the currently loaded snapshots.
It must be scoped to the intended batches when more snapshots exist.

