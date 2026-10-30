import os
import subprocess
import sys
from pathlib import Path

from dotenv import load_dotenv


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def main():
    load_dotenv(PROJECT_ROOT / ".env")

    required = (
        "POSTGRES_DB",
        "POSTGRES_USER",
        "POSTGRES_PASSWORD",
    )

    missing = [name for name in required if not os.getenv(name)]

    if missing:
        raise SystemExit(
            f"Missing database settings: {', '.join(missing)}"
        )

    os.environ["DBT_ENV_SECRET_POSTGRES_PASSWORD"] = (
        os.environ["POSTGRES_PASSWORD"]
    )

    dbt_executable = Path(sys.executable).parent / "dbt"

    if not dbt_executable.is_file():
        raise SystemExit(
            "dbt is not installed in this Python environment."
        )

    result = subprocess.run(
        [
            str(dbt_executable),
            *sys.argv[1:],
            "--project-dir",
            str(PROJECT_ROOT / "dbt"),
            "--profiles-dir",
            str(PROJECT_ROOT / "dbt"),
        ],
        cwd=PROJECT_ROOT,
    )

    raise SystemExit(result.returncode)


if __name__ == "__main__":
    main()
