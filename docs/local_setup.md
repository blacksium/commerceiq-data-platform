# Local Development Setup

## Purpose

Run the CommerceIQ PostgreSQL database locally and verify that
Python can connect to it.

## Prerequisites

- Python with virtual environment support.
- Docker Engine and Docker Compose.
- Git.

Verified development environment:
- Ubuntu 26.04.1 LTS.
- Python 3.14.4.
- PostgreSQL 17 container image.

Run commands from the repository root.

## Create the Python environment

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

For an existing environment, only activation is needed:

```bash
source .venv/bin/activate
```

## Configure local settings

On first setup, copy the example if .env does not already exist:

```bash
cp --update=none .env.example .env
```

Open .env and replace the password placeholder with a unique local
database password. Save it before starting PostgreSQL.

Do not commit .env or share its contents.

The POSTGRES settings initialize an empty database volume.
Editing .env later does not change an existing database password.

## Start PostgreSQL

```bash
docker compose config --quiet
docker compose up -d --wait
docker compose ps
```

PostgreSQL is published at 127.0.0.1:5432.

The named volume stores its database files separately from the container.

## Verify the Python connection

```bash
python scripts/check_db_connection.py
```

Expected output:

```text
Database connection successful.
Database: commerceiq
User: commerceiq_admin
```

The script loads settings from .env. Existing process environment
variables take precedence over values loaded from that file.

## Stop and resume

Stop the database while keeping the container and volume:

```bash
docker compose stop postgres
```

Resume it:

```bash
docker compose up -d --wait
```

Remove project containers and the network while keeping the volume:

```bash
docker compose down
```

Do not add -v unless intentionally deleting the database volume
and its saved data.

Leave the Python environment:

```bash
deactivate
```

Deactivating Python does not stop PostgreSQL.

## Troubleshooting

### Connection refused

Check that PostgreSQL is running and healthy:

```bash
docker compose ps
```

Confirm the Python host and port match the published Docker port.

### Password authentication failed

Check the local username and password.

If the volume was initialized previously, changing .env alone
does not update the stored database credentials.

### Missing Python package

Activate the project's .venv and install requirements.txt.

### Port already in use

Inspect listeners:

```bash
ss -ltn 'sport = :5432'
```

Identify the conflicting service before changing or stopping it.

## Verification completed

- Compose configuration validation passed.
- PostgreSQL reached healthy status.
- Password authentication through psql succeeded.
- Python connected and executed a query.
- A temporary record survived container removal and recreation.
- Stopping PostgreSQL caused the expected connection failure.
- Restarting PostgreSQL restored the Python connection.
- The temporary persistence test table was removed.