# Customer Staging

## Purpose

Prepare customer records for consistent joins with staged orders.

## Design

- Select the raw batch configured by customers_batch_id.
- Preserve all source records and loading metadata.
- Trim surrounding spaces and convert blanks to NULL.
- Keep customer identifiers and ZIP prefixes as text.
- Preserve repeated customer_unique_id values.
- Materialize staging.stg_customers as a view.

customer_id identifies the customer record referenced by an order.
customer_unique_id identifies customers across repeat orders.

## Verification

- Staged records: 99,441.
- Distinct customer IDs: 99,441.
- Distinct customer identities: 96,096.
- Combined orders/customer build: two views and 16 passing tests.
- Additional customer location-format test: passed separately.

Tests cover required customer fields, customer-ID uniqueness,
batch existence, row-count agreement, and orders-to-customers references.

ZIP prefixes must contain five digits.
State codes must contain two uppercase letters.
These are format checks, not geographic validity checks.

## Run

    python scripts/run_dbt.py build --select stg_orders stg_customers

With the current project, this selects two views and 17 tests.

## Snapshot selection

The customer and orders models use explicit batch UUIDs.
After recreating and reloading the database, update those variables
to the new registered batches before building.
