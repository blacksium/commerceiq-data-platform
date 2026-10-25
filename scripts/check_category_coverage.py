import csv
from collections import Counter
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIRECTORY = PROJECT_ROOT / "data" / "raw" / "olist"


def main():
    translation_file = (
        DATA_DIRECTORY / "product_category_name_translation.csv"
    )

    with translation_file.open(
        encoding="utf-8-sig", newline=""
    ) as file:
        translated_categories = {
            row["product_category_name"]
            for row in csv.DictReader(file)
            if row["product_category_name"].strip()
        }

    total_products = 0
    missing_category = 0
    matched_products = 0
    unmatched_categories = Counter()

    products_file = DATA_DIRECTORY / "olist_products_dataset.csv"

    with products_file.open(
        encoding="utf-8-sig", newline=""
    ) as file:
        for row in csv.DictReader(file):
            total_products += 1
            category = row["product_category_name"]

            if not category.strip():
                missing_category += 1
            elif category in translated_categories:
                matched_products += 1
            else:
                unmatched_categories[category] += 1

    unmatched_products = sum(unmatched_categories.values())

    print(f"Total products: {total_products:,}")
    print(f"Products without a category: {missing_category:,}")
    print(f"Products with a matching translation: {matched_products:,}")
    print(f"Products with an unmatched category: {unmatched_products:,}")
    print(f"Distinct unmatched categories: {len(unmatched_categories):,}")

    print("\nUnmatched categories:")
    for category, count in unmatched_categories.most_common():
        print(f"  {category}: {count:,} products")

    accounted_for = (
        missing_category + matched_products + unmatched_products
    )
    print(f"\nAll products accounted for: {accounted_for == total_products}")


if __name__ == "__main__":
    main()