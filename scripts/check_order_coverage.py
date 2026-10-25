import csv
from collections import Counter
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIRECTORY = PROJECT_ROOT / "data" / "raw" / "olist"


def load_order_statuses():
    path = DATA_DIRECTORY / "olist_orders_dataset.csv"

    with path.open(encoding="utf-8-sig", newline="") as file:
        return {
            row["order_id"]: row["order_status"]
            for row in csv.DictReader(file)
        }


def load_referenced_orders(filename):
    with (DATA_DIRECTORY / filename).open(
        encoding="utf-8-sig", newline=""
    ) as file:
        return {
            row["order_id"]
            for row in csv.DictReader(file)
            if row["order_id"].strip()
        }


def main():
    order_statuses = load_order_statuses()
    all_order_ids = set(order_statuses)

    sources = [
        ("items", "olist_order_items_dataset.csv"),
        ("payments", "olist_order_payments_dataset.csv"),
        ("reviews", "olist_order_reviews_dataset.csv"),
    ]

    for label, filename in sources:
        referenced_orders = load_referenced_orders(filename)
        missing_orders = all_order_ids - referenced_orders

        statuses = Counter(
            order_statuses[order_id]
            for order_id in missing_orders
        )

        print(f"\nOrders without {label}: {len(missing_orders):,}")

        for status, count in statuses.most_common():
            print(f"  {status}: {count:,}")


if __name__ == "__main__":
    main()