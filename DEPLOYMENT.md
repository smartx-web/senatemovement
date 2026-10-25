# Deployment preparation — senatemovement

No hosting service, database, domain, or production credentials have been created for this portal. Use a fresh database; do not reuse the NOPREM/betterbenue2027 or Solution2027 production databases or account settings.

## Render with a separate PostgreSQL database

The included `render.yaml` declares a Python web service named `senatemovement`, built with `pip install -r requirements.txt` and started with `python3 deploy.py`. Select the actual source repository, `smartx-web/senatemovement`, when creating the service. Deployment is not performed by local setup.

Provision a separate PostgreSQL database. Set the following securely in the hosting dashboard; never commit their values:

- `DATABASE_URL`: pooled PostgreSQL connection URL.
- `DATABASE_URL_UNPOOLED`: matching direct connection URL for migrations. Both connections must require TLS (`sslmode=require` or `verify-full`).
- `ADMIN_NAME`: your chosen initial administrator name.
- `ADMIN_PASSWORD_HASH`: generate privately with `python3 manage.py hash-password`. Keep the corresponding password private.
- `SENATE_MOVEMENT_ENV=production`: required; included in the Blueprint.
- `APP_ORIGIN`: canonical HTTPS URL; optional when Render supplies `RENDER_EXTERNAL_URL`.

Startup creates/migrates tables and loads the supplied district directory (1,373 PUs, 102 wards, 9 LGAs) and the separate Apa/Agatu historical aggregate baseline. Migration 003 restricts the LGA constraint to all nine Benue South LGAs. Verify PostgreSQL migrations in a disposable test database before production use. Bootstrap administrator variables are required only when no active administrator exists; remove the bootstrap hash after verifying initial access.

The service must run as **one process/instance** because sessions and login throttles are in memory. TLS is terminated by Render; do not expose Waitress directly to the public internet. Sessions end on restart. Photo uploads are stored in the database, not public filesystem storage.

## Checks before use

Verify `/healthz`, login, Secure cookies, CSRF rejection, account scopes, result submission/photo access, correction history, CSV exports, logout, and persistence after restart. The initial dataset should contain 1,373 PUs in 102 wards across all nine LGAs with a separate 2023 historical baseline of 131,035 registered voters. Location counts reflect the supplied file, not independent verification of current official completeness; the baseline is not a 2027 total.

Generate regular PostgreSQL backups with `python3 manage.py dump-postgres --output /secure/path/backup.dump`; configure the direct database URL privately. Use a compatible `pg_dump` client and verify restoration in a separate database. No recurring backup job is configured here.

For local SQLite, stop writes and use `python3 manage.py backup --output-dir /secure/path`. To transfer a SQLite copy, see `python3 manage.py migrate-sqlite --help`; the destination must be empty. Never delete live records to make room for a transfer.

## Optional live PostgreSQL integration checks

`test_postgres_integration.py` only accepts a local Unix socket and creates/drops disposable databases. It needs PostgreSQL 17+ and matching tools. Supply `SOLUTION_TEST_PG_SOCKET`, `SOLUTION_TEST_PG_PORT`, and `SOLUTION_TEST_PG_BIN` (test-only legacy names retained from upstream) before running `.venv/bin/python -m unittest -v`. Without them, five integration tests are explicitly skipped. Passing local tests does not establish hosted connectivity or deployment readiness.
