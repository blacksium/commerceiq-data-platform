# Business Requirements

## Project purpose

CommerceIQ is a data platform for a fictional e-commerce marketplace.

It will collect source data, check its quality, and prepare consistent
tables for business reporting.

## Business problems

- Teams manually combine separate order, payment, and delivery files.
- Reports can disagree because calculations use different rules.
- Payment differences are difficult to investigate.
- Delivery performance is difficult to compare across sellers.
- Failed data loads are difficult to trace and recover.

## Business users

| Team | Required information |
|---|---|
| Management | Daily orders, merchandise value, and sales trends |
| Finance | Recorded payment totals and reconciliation exceptions |
| Operations | Delivery delays and missing delivery milestones |
| Seller management | Seller sales and delivery performance |
| Analysts | Clean and documented reporting tables |

## Business questions

1. How many orders were placed each day?
2. What was the merchandise value of eligible orders?
3. How much payment value was recorded?
4. Which orders have differences between item prices plus freight
   and recorded payments?
5. What percentage of delivered orders arrived late?
6. Which sellers have the highest late-delivery rates?
7. Which product categories have the highest merchandise value?

## Data sources

The initial source is the public Olist e-commerce dataset.

We will review its files, structure, and usage terms before ingestion.

Later phases will add clearly labelled synthetic records to practise
new orders, status changes, late updates, and failure recovery.

## Planned outputs

- A PostgreSQL analytics warehouse.
- Tested SQL transformations managed with dbt.
- A scheduled pipeline managed with Airflow.
- Business reporting tables and a dashboard.
- Pipeline logs, quality results, and recovery instructions.
- An AWS deployment after the local pipeline works.

## Success criteria

- Source records can be traced to their loading batch.
- Reprocessing the same input does not duplicate business records.
- Invalid input produces a clear failure or recorded rejection.
- Reporting totals reconcile with independent source checks.
- New and changed records update correctly.
- Failed runs can be investigated and safely rerun.
- Business metrics have written definitions.
- Reports show the last successful data refresh.

## Scope limits

The project does not process real payments or verify bank settlement.

Merchandise value, freight charges, and recorded payment value will
remain separate metrics.

True profit and inventory analysis require additional data.

Historical source records and synthetic records will remain
distinguishable.
