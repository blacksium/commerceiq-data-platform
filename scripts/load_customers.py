import csv
import hashlib
import os
from pathlib import Path

import psycopg
from dotenv import load_dotenv
from uuid import uuid4

PROJECT_ROOT = Path(__file__).resolve().parents[1]

SOURCE_FILE = (
    PROJECT_ROOT / "data" / "raw" / "olist" / "olist_customers_dataset.csv"
)

EXPECTED_COLUMNS = [
    "customer_id",
    "customer_unique_id",
    "customer_zip_code_prefix",
    "customer_city",
    "customer_state",
]


def calculate_sha256(file_path):
    digest = hashlib.sha256()

    with file_path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)

    return digest.hexdigest()


def validate_csv(file_path):
    with file_path.open("r", encoding="utf-8", newline="") as source:
        reader = csv.reader(source, strict=True)
        header = next(reader, None)

        if header != EXPECTED_COLUMNS:
            raise ValueError(
                f"Unexpected CSV columns.\n"
                f"Expected: {EXPECTED_COLUMNS}\n"
                f"Received: {header}"
            )

        row_count = 0

        for row_number, row in enumerate(reader, start=1):
            if len(row) != len(EXPECTED_COLUMNS):
                raise ValueError(
                    f"Source record {row_number} has {len(row)} fields; "
                    f"expected {len(EXPECTED_COLUMNS)}."
                )

            row_count += 1

    if row_count == 0:
        raise ValueError("The customers CSV contains no data records.")

    return row_count


def get_connection():
    load_dotenv(PROJECT_ROOT / ".env")

    required_settings = (
        "POSTGRES_DB",
        "POSTGRES_USER",
        "POSTGRES_PASSWORD",
    )

    missing = [
        name for name in required_settings
        if not os.getenv(name)
    ]

    if missing:
        raise ValueError(
            f"Missing database settings: {', '.join(missing)}"
        )

    return psycopg.connect(
        host="127.0.0.1",
        port=5432,
        dbname=os.environ["POSTGRES_DB"],
        user=os.environ["POSTGRES_USER"],
        password=os.environ["POSTGRES_PASSWORD"],
        connect_timeout=5,
    )

def load_customers(connection, file_sha256, expected_count):
    batch_id = uuid4()

    with connection.cursor() as cursor:
        cursor.execute(
            """
            INSERT INTO raw.load_batches (
                batch_id,
                source_name,
                source_file,
                file_sha256,
                row_count
            )
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (source_name, file_sha256) DO NOTHING
            RETURNING batch_id
            """,
            (
                batch_id,
                "olist_customers",
                SOURCE_FILE.name,
                file_sha256,
                expected_count,
            ),
        )

        if cursor.fetchone() is None:
            return None

        with SOURCE_FILE.open(
            "r", encoding="utf-8", newline=""
        ) as source:
            reader = csv.reader(source, strict=True)

            if next(reader, None) != EXPECTED_COLUMNS:
                raise ValueError("CSV header changed before loading.")

            copied_count = 0

            with cursor.copy(
                 """
                COPY raw.customers (
                    batch_id,
                    source_row_number,
                    source_file,
                    customer_id,
                    customer_unique_id,
                    customer_zip_code_prefix,
                    customer_city,
                    customer_state
                )
                FROM STDIN
                """
            ) as copy:
                for row_number, row in enumerate(reader, start=1):
                    if len(row) != len(EXPECTED_COLUMNS):
                        raise ValueError(
                            f"Invalid field count at record {row_number}."
                        )

                    copy.write_row(
                        (batch_id, row_number, SOURCE_FILE.name, *row)
                    )

                    copied_count += 1

        if copied_count != expected_count:
            raise ValueError(
                f"Expected {expected_count} records, "
                f"but copied {copied_count}."
            )

        if calculate_sha256(SOURCE_FILE) != file_sha256:
            raise ValueError("Source file changed during loading.")

        cursor.execute(
            """
            SELECT COUNT(*)
            FROM raw.customers
            WHERE batch_id = %s
            """,
            (batch_id,),
        )

        database_count = cursor.fetchone()[0]

        if database_count != expected_count:
            raise ValueError(
                f"Expected {expected_count} database records, "
                f"but found {database_count}."
            )

    return batch_id

def main():
    if not SOURCE_FILE.is_file():
        raise SystemExit(f"Source file not found: {SOURCE_FILE}")

    file_sha256 = calculate_sha256(SOURCE_FILE)
    row_count = validate_csv(SOURCE_FILE)

    print(f"Source file: {SOURCE_FILE.name}")
    print(f"SHA256: {file_sha256}")
    print(f"Validated data records: {row_count:,}")

    with get_connection() as connection:
        batch_id = load_customers(connection, file_sha256, row_count)

    if batch_id is None:
        print("This file was already loaded. No records inserted.")
        return

    print("Load committed successfully.")
    print(f"Batch ID: {batch_id}")
    print(f"Loaded records: {row_count:,}")


if __name__ == "__main__":
    main()
