# Data Quality Findings

## Orders file profile

Source: data/raw/olist/olist_orders_dataset.csv

- Rows: 99,441
- Distinct order IDs: 99,441
- Repeated order IDs: 0
- Missing order IDs: 0
- Missing customer IDs: 0

Observed grain: one row per order.
Candidate primary key: order_id.

These findings describe the current source file.
Future loads must repeat the relevant checks.

## DQ001 Delivered orders missing delivery timestamps

Severity: warning.

Observed result:
8 orders have order_status = delivered and a blank
order_delivered_customer_date.

Business impact:
Delivery duration and lateness cannot be determined reliably
for these records.

Handling:
- Preserve the source records.
- Flag them for review.
- Exclude them from delivery duration and late-delivery calculations.
- Report the excluded-record count alongside those metrics.
- Allow them in counts explicitly defined as orders marked delivered.

## Follow up investigation

6 canceled orders have a nonblank customer delivery timestamp.

Inspect these records before deciding whether this represents
a valid business situation or inconsistent source data.

## Review key assessment

Source: data/raw/olist/olist_order_reviews_dataset.csv

- Rows: 99,224
- Distinct review IDs: 98,410
- Distinct order IDs: 98,673
- Distinct review ID and order ID pairs: 99,224
- Missing composite key fields: 0
- Repeated composite keys: 0

Candidate composite key: (review_id, order_id).

Neither review_id nor order_id is unique by itself.

Preserve all source review records. Do not remove rows merely because
one of these identifiers repeats.

Reports requiring one row per order must apply a documented review
selection or aggregation rule before joining.


## Source relationship checks

All six checked relationships had zero blank references and zero
orphan rows:

- Orders to customers.
- Order items to orders.
- Order items to products.
- Order items to sellers.
- Payments to orders.
- Reviews to orders.

These checks establish child-to-parent validity for the current files.
They do not establish that every order has related detail records.

## Order detail coverage

### Orders without items

775 orders have no item records:

- unavailable: 603
- canceled: 164
- created: 5
- invoiced: 2
- shipped: 1

Preserve these orders. Investigate the shipped and invoiced records
before deciding on status-specific quality rules.

No delivered orders were missing item records in this check.

### Orders without payments

1 delivered order has no payment record.

Flag it for reconciliation review. Missing source data does not prove
that payment was not made.

Preserve a missing-payment flag rather than treating absence as a
confirmed payment value of zero.

### Orders without reviews

768 orders have no review records:

- delivered: 646
- shipped: 75
- canceled: 20
- unavailable: 14
- processing: 6
- invoiced: 5
- created: 2

Preserve these orders in order reporting.

Calculate review metrics using available valid reviews and disclose
review coverage. Do not assume the reason a review is absent.

## Join design implications

Use joins appropriate to the reporting population.

An inner join can silently exclude orders with missing details.
A left join preserves orders but requires explicit missing-data handling.

Aggregate item, payment, and review details to the required grain
before combining them into an order-level report.


## Category translation coverage

Products checked: 32,951.

- Matching category translation: 32,328 products.
- Missing source category: 610 products.
- Nonblank category without a translation: 13 products.

Unmatched source categories:

- portateis_cozinha_e_preparadores_de_alimentos: 10 products.
- pc_gamer: 3 products.

The three outcome groups reconcile to the total product count.

Handling:
- Preserve all products during translation enrichment using a left join.
- Keep the original category label.
- Distinguish missing source categories from missing translations.
- Record any future manual translations in a separate documented mapping.


## Remaining validation work

Initial discovery covered row counts, blank values, candidate keys,
six source relationships, order detail coverage, and category
translation coverage.

The following checks remain for later validation work:

- Parse timestamps and investigate impossible event sequences.
- Validate monetary values, installments, scores, and physical dimensions.
- Check customer and seller ZIP coverage against geography.
- Investigate full-row duplicates in geography.
- Inspect canceled orders with delivery timestamps.
- Inspect shipped and invoiced orders without items.
- Investigate the delivered order without a payment record.
- Define review selection or aggregation rules for order-level reports.
- Confirm source timezone and monetary-unit conventions before
  publishing related metrics.

Proposed data types and handling rules are not proof that source
values satisfy them.

These limitations must be considered when implementing ingestion,
transformations, and reporting.
