import os
from pathlib import Path

import psycopg
from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parents[1]


def main():
    load_dotenv(PROJECT_ROOT / ".env")

    required_settings = (
        "POSTGRES_DB",
        "POSTGRES_USER",
        "POSTGRES_PASSWORD",
    )

    missing = [
        name
        for name in required_settings
        if not os.getenv(name)
    ]

    if missing:
        raise SystemExit(
            f"Missing required settings: {', '.join(missing)}"
        )

    with psycopg.connect(
        host="127.0.0.1",
        port=5432,
        dbname=os.environ["POSTGRES_DB"],
        user=os.environ["POSTGRES_USER"],
        password=os.environ["POSTGRES_PASSWORD"],
        connect_timeout=5,
    ) as connection:
        with connection.cursor () as cursor:
            cursor.execute(
                "SELECT current_database(), current_user;"
            )
            database, user = cursor.fetchone()

    print("Database connection successful.")
    print(f"Database: {database}")
    print(f"User: {user}")

if __name__ == "__main__":
    main()