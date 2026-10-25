import csv
from collections import Counter
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIRECTORY = PROJECT_ROOT / "data" / "raw" / "olist"


def profile_file(path):
    row_count = 0
    missing = Counter()

    with path.open(encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)
        columns = reader.fieldnames or []

        for row in reader:
            row_count += 1

            for column in columns:
                value = row.get(column)
                if value is None or not value.strip():
                    missing[column] += 1

    print(f"\nFILE: {path.name}")
    print(f"Rows: {row_count:,}")
    print(f"Columns: {len(columns)}")

    for column in columns:
        count = missing[column]
        percentage = count / row_count * 100 if row_count else 0
        print(
            f"  {column}: "
            f"{count:,} missing ({percentage:.2f}%)"
        )


def main():
    paths = sorted(DATA_DIRECTORY.glob("*.csv"))

    if not paths:
        raise SystemExit(f"No CSV files found in {DATA_DIRECTORY}")

    for path in paths:
        profile_file(path)


if __name__ == "__main__":
    main()