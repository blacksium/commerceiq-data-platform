import argparse
import csv
import hashlib
import os
from pathlib import Path
from uuid import uuid4

import psycopg
from dotenv import load_dotenv
from psycopg import sql

from scripts.source_config import SOURCES


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def calculate_sha256(path):
    digest = hashlib.sha256()

    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)

    return digest.hexdigest()


def validate_csv(path, columns):
    with path.open("r", encoding="utf-8-sig", newline="") as source:
        reader = csv.reader(source, strict=True)

        if next(reader, None) != columns:
            raise ValueError(f"Unexpected CSV header: {path.name}")

        count = 0

        for number, row in enumerate(reader, start=1):
            if len(row) != len(columns):
                raise ValueError(
                    f"{path.name}: invalid field count at record {number}."
                )

            count += 1

    if count == 0:
        raise ValueError(f"No data records: {path.name}")

    return count


def get_connection():
    load_dotenv(PROJECT_ROOT / ".env")

    required = (
        "POSTGRES_DB",
        "POSTGRES_USER",
        "POSTGRES_PASSWORD",
    )

    missing = [name for name in required if not os.getenv(name)]

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


def load_source(connection, config, path, fingerprint, expected_count):
    batch_id = uuid4()
    target = sql.Identifier("raw", config["table"])

    copy_columns = [
        "batch_id",
        "source_row_number",
        "source_file",
        *config["columns"],
    ]

    copy_statement = sql.SQL(
        "COPY {} ({}) FROM STDIN"
    ).format(
        target,
        sql.SQL(", ").join(
            sql.Identifier(column) for column in copy_columns
        ),
    )

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
                config["source_name"],
                path.name,
                fingerprint,
                expected_count,
            ),
        )

        if cursor.fetchone() is None:
            return None

        with path.open(
            "r", encoding="utf-8-sig", newline=""
        ) as source:
            reader = csv.reader(source, strict=True)

            if next(reader, None) != config["columns"]:
                raise ValueError("CSV header changed before loading.")

            copied_count = 0

            with cursor.copy(copy_statement) as copy:
                for number, row in enumerate(reader, start=1):
                    if len(row) != len(config["columns"]):
                        raise ValueError(
                            f"Invalid field count at record {number}."
                        )

                    copy.write_row(
                        (batch_id, number, path.name, *row)
                    )

                    copied_count += 1

        if copied_count != expected_count:
            raise ValueError(
                f"Expected {expected_count} records, "
                f"but copied {copied_count}."
            )

        if calculate_sha256(path) != fingerprint:
            raise ValueError("Source file changed during loading.")

        cursor.execute(
            sql.SQL(
                "SELECT COUNT(*) FROM {} WHERE batch_id = %s"
            ).format(target),
            (batch_id,),
        )

        stored_count = cursor.fetchone()[0]

        if stored_count != expected_count:
            raise ValueError(
                f"Expected {expected_count} database records, "
                f"but found {stored_count}."
            )

    return batch_id


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Load one configured Olist CSV into PostgreSQL."
    )

    parser.add_argument(
        "source",
        choices=sorted(SOURCES),
        help="Dataset to load.",
    )

    args = parser.parse_args(argv)
    config = SOURCES[args.source]
    path = PROJECT_ROOT / "data" / "raw" / "olist" / config["filename"]

    if not path.is_file():
        raise SystemExit(f"Source file not found: {path}")

    fingerprint = calculate_sha256(path)
    count = validate_csv(path, config["columns"])

    print(f"Source: {args.source}")
    print(f"File: {path.name}")
    print(f"SHA256: {fingerprint}")
    print(f"Validated data records: {count:,}")

    with get_connection() as connection:
        batch_id = load_source(
            connection, config, path, fingerprint, count
        )

    if batch_id is None:
        print("This file was already loaded. No records inserted.")
        return

    print("Load committed successfully.")
    print(f"Batch ID: {batch_id}")
    print(f"Loaded records: {count:,}")


if __name__ == "__main__":
    main()
