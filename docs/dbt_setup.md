# dbt Staging Foundation

## Purpose

Transform preserved raw text into typed staging models.
Keep raw tables unchanged and retain loading metadata.

## Environment

- Python 3.14.4
- dbt Core 1.12.6
- dbt PostgreSQL adapter 1.11.0
- PostgreSQL 17

Install with the project virtual environment active:

    python -m pip install -r requirements-dbt.txt

The parser dependency required a separate resumable download during
initial setup because its GitHub download timed out.

## Project files

- dbt/dbt_project.yml: project settings and selected orders batch.
- dbt/profiles.yml: connection settings using environment variables.
- scripts/run_dbt.py: loads .env and launches the environment's dbt.
- dbt/models/staging/sources.yml: existing raw input tables.
- dbt/models/staging/stg_orders.sql: orders transformation.
- dbt/models/staging/stg_orders.yml: column tests.
- dbt/tests/assert_orders_batch_and_count.sql: batch/count test.

Actual credentials remain in the ignored .env file.
Do not put password values in profiles.yml.

## Commands

Run from the project root with .venv active and PostgreSQL running.

Check connectivity:

    python scripts/run_dbt.py debug

Build and test orders:

    python scripts/run_dbt.py build --select stg_orders

## Orders transformation

- Select one explicit batch using the orders_batch_id variable.
- Preserve batch ID, source record number, filename and load timestamp.
- Trim surrounding spaces from source fields.
- Convert empty strings to NULL.
- Cast source timestamps to timestamp without time zone.
- Do not claim the source timestamps are UTC.
- Preserve records with missing delivery dates.
- Materialize the model as staging.stg_orders, a view.

The view reads its underlying raw records when queried.
Creating the view alone does not validate every timestamp value.

## Verification

Before transformation, all five timestamp columns had zero invalid
nonblank inputs according to PostgreSQL timestamp input validation.

- Orders: 99,441.
- Distinct order IDs: 99,441.
- Missing delivery timestamps: 2,965.
- First purchase: 2016-09-04 21:15:19.
- Last purchase: 2018-10-17 17:30:18.
- Build result: one view and eight passing data tests.

Tests cover required fields, unique order IDs, allowed statuses,
selected batch existence and agreement with its registered row count.

Business chronology and delivery inconsistencies need further checks.
The known eight delivered orders without delivery timestamps remain
in staging and require explicit handling in later delivery metrics.
