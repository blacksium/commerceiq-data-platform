# Source Data Dictionary

## Purpose

Describe the source tables, their observed grain, candidate keys,
and field meanings.

Counts and key findings describe the downloaded source snapshot.
They must be checked again when new data arrives.

All CSV fields are initially read as text. The proposed types below
describe how we intend to represent them after validation.

## Orders

Source file: olist_orders_dataset.csv
Observed rows: 99,441
Grain: one row per order
Candidate primary key: order_id

Relationship:
customer_id references customer_id in olist_customers_dataset.csv.

| Column | Meaning | Proposed type | Notes |
|---|---|---|---|
| order_id | Source identifier for an order | Text | Unique and nonblank in this snapshot |
| customer_id | Reference to the source customer record | Text | Nonblank; all references matched customers |
| order_status | Recorded order lifecycle status | Text | Eight distinct statuses observed |
| order_purchase_timestamp | Recorded purchase date and time | Timestamp | No blanks observed |
| order_approved_at | Recorded payment approval date and time | Nullable timestamp | 160 blanks observed |
| order_delivered_carrier_date | Recorded handoff date and time to the logistics partner | Nullable timestamp | 1,783 blanks observed |
| order_delivered_customer_date | Recorded customer delivery date and time | Nullable timestamp | 2,965 blanks; includes 8 delivered orders |
| order_estimated_delivery_date | Estimated delivery date supplied by the source | Timestamp | No blanks observed |

### Observed statuses

- delivered
- shipped
- canceled
- unavailable
- invoiced
- processing
- created
- approved

### Handling notes

- Preserve all source orders.
- Do not treat missing timestamps as zero or replace them with today's date.
- Validate timestamp parsing and chronology before calculating durations.
- Do not assign a timezone without verifying the source convention.
- Keep orders with missing item, payment, or review records visible
  where the reporting population requires them.
- See data_quality_findings.md for observed exceptions and handling decisions.


## Customers

Source file: olist_customers_dataset.csv
Observed rows: 99,441
Grain: one row per source customer_id
Candidate primary key: customer_id

Relationship:
Orders reference this table using customer_id.

| Column | Meaning | Proposed type | Notes |
|---|---|---|---|
| customer_id | Identifier for the customer record referenced by an order | Text | 99,441 distinct values; no blanks |
| customer_unique_id | Identifier used to recognize a customer across orders | Text | 96,096 distinct values; repeats across customer records |
| customer_zip_code_prefix | First part of the customer's postal code | Text | Preserve leading zeros |
| customer_city | Customer city supplied by the source | Text | No blanks; spelling consistency not yet checked |
| customer_state | Customer state abbreviation supplied by the source | Text | No blanks; accepted values not yet validated |

### Handling notes

- Join orders to customers using customer_id.
- Count distinct customer_unique_id values for customer-level reporting.
- Do not remove rows merely because customer_unique_id repeats.
- Keep ZIP prefixes as text because they are labels, not quantities.
- Do not join directly to raw geography assuming one row per ZIP prefix.
- No blank fields were observed, but other validity checks are still needed.


## Order items

Source file: olist_order_items_dataset.csv
Observed rows: 112,650
Grain: one item entry within an order
Candidate composite key: (order_id, order_item_id)

Relationships:
- order_id references orders.order_id.
- product_id references products.product_id.
- seller_id references sellers.seller_id.

All three relationships passed the source reference checks.

| Column | Meaning | Proposed type | Notes |
|---|---|---|---|
| order_id | Order containing the item | Text | Can repeat across item rows |
| order_item_id | Item sequence number within the order | Integer | Unique only when combined with order_id |
| product_id | Product referenced by the item | Text | All references matched products |
| seller_id | Seller associated with the item | Text | All references matched sellers |
| shipping_limit_date | Source shipping deadline for the item | Timestamp | Parsing and chronology not yet validated |
| price | Item price recorded by the source | Decimal | Validate numeric format and range |
| freight_value | Freight charge recorded for the item | Decimal | Keep separate from merchandise value |

### Handling notes

- Preserve the item-level grain.
- Do not treat order_item_id as a quantity or a globally unique ID.
- Use exact decimal arithmetic for monetary calculations.
- Aggregate items to order level before comparing with order payments.
- No blank fields were observed in this snapshot.

## Order payments

Source file: olist_order_payments_dataset.csv
Observed rows: 103,886
Grain: one payment entry within an order
Candidate composite key: (order_id, payment_sequential)

Relationship:
order_id references orders.order_id.

All payment references matched existing orders.

| Column | Meaning | Proposed type | Notes |
|---|---|---|---|
| order_id | Order associated with the payment entry | Text | Can repeat across payment rows |
| payment_sequential | Sequence identifying a payment entry within an order | Integer | Combine with order_id for uniqueness |
| payment_type | Payment method recorded by the source | Text | Accepted values not yet profiled |
| payment_installments | Number of installments recorded for the payment | Integer | Validate values before interpretation |
| payment_value | Value recorded for this payment entry | Decimal | Validate numeric format and range |

### Handling notes

- Multiple payment entries can belong to one order.
- payment_sequential and payment_installments represent different concepts.
- Do not multiply payment_value by payment_installments when calculating
  recorded payment totals.
- Aggregate payment_value by order_id for order-level reconciliation.
- One delivered order has no payment record.
- Preserve missing-payment information separately from a zero payment value.
- No blank fields were observed in this snapshot.


## Products

Source file: olist_products_dataset.csv
Observed rows: 32,951
Grain: one row per product
Candidate primary key: product_id

Relationship:
Order items reference this table using product_id.

| Column | Meaning | Proposed type | Notes |
|---|---|---|---|
| product_id | Source product identifier | Text | Unique and nonblank in this snapshot |
| product_category_name | Source category name | Nullable text | 610 blanks |
| product_name_lenght | Recorded product name length | Nullable integer | 610 blanks; preserve source spelling in raw data |
| product_description_lenght | Recorded product description length | Nullable integer | 610 blanks; preserve source spelling in raw data |
| product_photos_qty | Recorded number of product photos | Nullable integer | 610 blanks |
| product_weight_g | Product weight in grams | Nullable decimal | 2 blanks; numeric values not yet validated |
| product_length_cm | Product length in centimeters | Nullable decimal | 2 blanks |
| product_height_cm | Product height in centimeters | Nullable decimal | 2 blanks |
| product_width_cm | Product width in centimeters | Nullable decimal | 2 blanks |

### Handling notes

- Preserve products with missing categories or physical attributes.
- Keep missing categories distinguishable in category reporting.
- Matching missing-value counts do not prove the same rows are affected.
- Preserve original column names in raw data.
- Later staging models may rename lenght to length explicitly.
- Validate numeric formats, ranges, and units before calculations.

## Sellers

Source file: olist_sellers_dataset.csv
Observed rows: 3,095
Grain: one row per seller
Candidate primary key: seller_id

Relationship:
Order items reference this table using seller_id.

| Column | Meaning | Proposed type | Notes |
|---|---|---|---|
| seller_id | Source seller identifier | Text | Unique and nonblank in this snapshot |
| seller_zip_code_prefix | First part of the seller postal code | Text | Preserve leading zeros |
| seller_city | Seller city supplied by the source | Text | Spelling consistency not yet checked |
| seller_state | Seller state abbreviation supplied by the source | Text | Accepted values not yet validated |

### Handling notes

- No blank seller fields were observed.
- All seller references from order items matched this table.
- An order can contain items from different sellers.
- Do not assume one seller per order.
- Raw geography can contain several rows per ZIP prefix.


## Reviews

Source file: olist_order_reviews_dataset.csv
Observed rows: 99,224
Grain: one source review and order association
Candidate composite key: (review_id, order_id)

Relationship:
order_id references orders.order_id.

All review order references matched existing orders.

| Column | Meaning | Proposed type | Notes |
|---|---|---|---|
| review_id | Source review identifier | Text | Repeats when checked alone |
| order_id | Order associated with the review | Text | Some orders have multiple review rows |
| review_score | Customer rating recorded by the source | Integer | Validate the expected range of 1 to 5 |
| review_comment_title | Optional review title | Nullable text | 87,658 blanks |
| review_comment_message | Optional review message | Nullable text | 58,274 blanks |
| review_creation_date | Source date associated with creation of the review request | Timestamp | Do not assume this is the submission time |
| review_answer_timestamp | Recorded review answer timestamp | Timestamp | Parsing and chronology not yet validated |

### Handling notes

- The combination of review_id and order_id is unique in this snapshot.
- Do not remove rows solely because either identifier repeats.
- Missing written comments do not automatically invalidate a score.
- Preserve orders without reviews in order reporting.
- Define a selection or aggregation rule when a report needs one
  review result per order.
- Avoid multiplying order totals by joining directly to review details.

## Geography

Source file: olist_geolocation_dataset.csv
Observed rows: 1,000,163
Grain: one source geolocation record
Primary key: not established

Observed distinct ZIP prefixes: 19,015.

| Column | Meaning | Proposed type | Notes |
|---|---|---|---|
| geolocation_zip_code_prefix | First part of a postal code | Text | Repeats; preserve leading zeros |
| geolocation_lat | Latitude recorded by the source | Decimal | Coordinate ranges not yet validated |
| geolocation_lng | Longitude recorded by the source | Decimal | Coordinate ranges not yet validated |
| geolocation_city | City recorded by the source | Text | Spelling consistency not yet checked |
| geolocation_state | State abbreviation recorded by the source | Text | Accepted values not yet validated |

### Handling notes

- No blank fields were observed.
- A ZIP prefix is not a unique row identifier.
- Full-row duplicate checks have not yet been performed.
- Direct joins on ZIP prefix can multiply customer or seller rows.
- If reporting needs one row per ZIP prefix, build a separate reference
  using a documented coordinate and location-selection policy.
- Customer and seller ZIP coverage has not yet been checked.

## Category translations

Source file: product_category_name_translation.csv
Observed rows: 71
Grain: one source category translation
Candidate primary key: product_category_name

Proposed relationship:
Products can be enriched by matching product_category_name.

Coverage checked: 32,328 products matched a translation.
610 products had no category, and 13 products had a nonblank category
without a matching translation.

| Column | Meaning | Proposed type | Notes |
|---|---|---|---|
| product_category_name | Source category label | Text | Unique and nonblank in this snapshot |
| product_category_name_english | English category label supplied by the source | Text | No blanks observed |

### Handling notes

- Preserve the original category alongside its English label.
- Distinguish a missing product category from a missing translation.
- Use a left join when enriching products so unmatched categories
  do not silently remove products.