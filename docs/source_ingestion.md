# Source Ingestion

## Purpose

Load all nine Olist CSV files into PostgreSQL raw tables.
Preserve source values and track each completed file load.

## Files

- scripts/source_config.py: filenames, source names, tables and columns.
- scripts/load_source.py: shared validation and loading logic.
- scripts/load_orders.py: entry point for orders.
- scripts/load_customers.py: entry point for customers.
- sql/001 through sql/004: raw schema and table definitions.

## Setup

Run commands from the project root.

1. Activate .venv and install requirements.txt.
2. Configure database credentials in the ignored .env file.
3. Start PostgreSQL with docker compose up -d --wait.
4. Apply SQL files 001 through 004 in numerical order.

Apply each SQL file with:

    docker compose exec -T postgres psql -U commerceiq_admin -d commerceiq -v ON_ERROR_STOP=1 --single-transaction < sql/FILE.sql

Replace FILE.sql with the actual filename.

## Load a dataset

    python -m scripts.load_source products

Available dataset names:

- orders
- customers
- order_items
- order_payments
- order_reviews
- products
- sellers
- geolocation
- category_translation

The existing orders and customers script commands also remain supported.

## Loading behaviour

- Validate the expected header and number of fields per record.
- Reject files with no data records.
- Read CSV text with utf-8-sig to handle the translation file's BOM.
- Calculate SHA256 from the original file bytes.
- Preserve source fields as text, including empty strings.
- Register a batch using the source name and file fingerprint.
- Skip a file already registered for that source.
- Load records using PostgreSQL COPY.
- Verify copied and stored counts and recheck the file fingerprint.
- Commit the batch registration and records together.
- Roll back both if an error escapes the transaction.

Each file has its own transaction. A failure does not undo previously
completed files.

## Initial load verification

| Dataset | Stored records |
| --- | ---: |
| Orders | 99,441 |
| Customers | 99,441 |
| Order items | 112,650 |
| Order payments | 103,886 |
| Order reviews | 99,224 |
| Products | 32,951 |
| Sellers | 3,095 |
| Geolocation | 1,000,163 |
| Category translation | 71 |

All nine tables matched their registered batch counts.
Each table contained one batch during this verification.

Existing orders and customers were skipped by the shared loader.
Both original entry-point commands were also verified to skip them.

A temporary one-record customer file was loaded while expecting two
records. The expected error rolled back the attempt. Counts remained
99,441 customers and nine total batches, with no test batch remaining.

## Boundaries

These checks verify ingestion, not every business rule or source value.

Changed file contents create a new batch. Old batches remain stored.
Downstream queries must select the intended snapshots.

The current orders table has no batch foreign key.
Customers and the seven tables created by SQL 004 have batch foreign keys.

Further validation, typed fields, joins and business metrics belong
to the transformation work.
