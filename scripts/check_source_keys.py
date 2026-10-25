import csv
from collections import Counter
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIRECTORY = PROJECT_ROOT / "data" / "raw" / "olist"

CHECKS = [
    ("olist_orders_dataset.csv", ("order_id",)),
    ("olist_customers_dataset.csv", ("customer_id",)),
    ("olist_customers_dataset.csv", ("customer_unique_id",)),
    ("olist_order_items_dataset.csv", ("order_id", "order_item_id")),
    (
        "olist_order_payments_dataset.csv",
        ("order_id", "payment_sequential"),
    ),
    ("olist_order_reviews_dataset.csv", ("review_id",)),
    ("olist_order_reviews_dataset.csv", ("order_id",)),
    ("olist_order_reviews_dataset.csv", ("review_id", "order_id")),
    ("olist_products_dataset.csv", ("product_id",)),
    ("olist_sellers_dataset.csv", ("seller_id",)),
    ("product_category_name_translation.csv", ("product_category_name",)),
    ("olist_geolocation_dataset.csv", ("geolocation_zip_code_prefix",)),
]


def check_key(filename, columns):
    counts = Counter()
    missing_key_rows = 0
    total_rows = 0

    with (DATA_DIRECTORY / filename).open(
        encoding="utf-8-sig", newline=""
    ) as file:
        reader = csv.DictReader(file)

        for row in reader:
            total_rows += 1
            key = tuple(row[column] for column in columns)

            if any(not value.strip() for value in key):
                missing_key_rows += 1
                continue

            counts[key] += 1

    repeated_keys = sum(count > 1 for count in counts.values())
    extra_rows = sum(count - 1 for count in counts.values())

    print(f"\nFILE: {filename}")
    print(f"Key columns: {', '.join(columns)}")
    print(f"Total rows: {total_rows:,}")
    print(f"Rows with missing key fields: {missing_key_rows:,}")
    print(f"Distinct nonblank keys: {len(counts):,}")
    print(f"Keys appearing more than once: {repeated_keys:,}")
    print(f"Extra rows beyond one per key: {extra_rows:,}")


def main():
    for filename, columns in CHECKS:
        check_key(filename, columns)


if __name__ == "__main__":
    main()