import csv
from collections import Counter
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
ORDERS_FILE = (
    PROJECT_ROOT / "data" / "raw" / "olist"
    / "olist_orders_dataset.csv"
)


def main():
    order_ids = Counter()
    statuses = Counter()
    missing = Counter()
    missing_delivery_by_status = Counter()
    row_count = 0

    with ORDERS_FILE.open(encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)
        columns = reader.fieldnames or []

        print("Columns:")
        for column in columns:
            print(f"  {column}")

        for row in reader:
            row_count += 1
            order_ids[row["order_id"]] += 1
            statuses[row["order_status"]] += 1
            if not row["order_delivered_customer_date"].strip():
                missing_delivery_by_status[row["order_status"]] +=1

            for column in columns:
                if not row[column].strip():
                    missing[column] += 1


    duplicate_ids = sum(
        count > 1 for count in order_ids.values()
    )

    print(f"\nTotal rows: {row_count:,}")
    print(f"Distinct order IDs: {len(order_ids):,}")
    print(f"Order IDs appearing more than once: {duplicate_ids:,}")

    print("\nOrder statuses:")
    for status, count in statuses.most_common():
        print(f"  {status}: {count:,}")

    print("\nMissing values:")
    for column in columns:
        print(f"  {column}: {missing[column]:,}")

    print("\nMissing customer delivery dates by status:")
    for status, count in missing_delivery_by_status.most_common():
        print(f"  {status}: {count:,}")


if __name__ == "__main__":
    main()