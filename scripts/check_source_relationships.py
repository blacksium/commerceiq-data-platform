import csv
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIRECTORY = PROJECT_ROOT / "data" / "raw" / "olist"


def load_ids(filename, column):
    with (DATA_DIRECTORY / filename).open(
        encoding="utf-8-sig", newline=""
    ) as file:
        return {
            row[column]
            for row in csv.DictReader(file)
            if row[column].strip()
        }


def check_relationship(filename, column, parent_ids, parent_name):
    total_rows = 0
    blank_rows = 0
    orphan_rows = 0
    orphan_ids = set()

    with (DATA_DIRECTORY / filename).open(
        encoding="utf-8-sig", newline=""
    ) as file:
        for row in csv.DictReader(file):
            total_rows += 1
            value = row[column]

            if not value.strip():
                blank_rows += 1
            elif value not in parent_ids:
                orphan_rows += 1
                orphan_ids.add(value)

    print(f"\nCHECK: {filename}.{column} -> {parent_name}")
    print(f"Rows checked: {total_rows:,}")
    print(f"Blank references: {blank_rows:,}")
    print(f"Orphan rows: {orphan_rows:,}")
    print(f"Distinct orphan IDs: {len(orphan_ids):,}")


def main():
    customer_ids = load_ids("olist_customers_dataset.csv", "customer_id")
    order_ids = load_ids("olist_orders_dataset.csv", "order_id")
    product_ids = load_ids("olist_products_dataset.csv", "product_id")
    seller_ids = load_ids("olist_sellers_dataset.csv", "seller_id")

    checks = [
        (
            "olist_orders_dataset.csv", "customer_id",
            customer_ids, "customers.customer_id",
        ),
        (
            "olist_order_items_dataset.csv", "order_id",
            order_ids, "orders.order_id",
        ),
        (
            "olist_order_items_dataset.csv", "product_id",
            product_ids, "products.product_id",
        ),
        (
            "olist_order_items_dataset.csv", "seller_id",
            seller_ids, "sellers.seller_id",
        ),
        (
            "olist_order_payments_dataset.csv", "order_id",
            order_ids, "orders.order_id",
        ),
        (
            "olist_order_reviews_dataset.csv", "order_id",
            order_ids, "orders.order_id",
        ),
    ]

    for filename, column, parent_ids, parent_name in checks:
        check_relationship(filename, column, parent_ids, parent_name)


if __name__ == "__main__":
    main()