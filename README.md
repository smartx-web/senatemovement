# Senate Movement for Olofu 2027

Benue South coordination portal adapted from smartx-web/NOPREM (betterbenue2027). Includes polling units, consenting agent assignments, field reports, CSV import/export, activity history, role-based accounts, and polling-unit results with photos, revisions and internal verification.

## Run locally

Requires Python 3.12+; Python 3.12 is verified.

```sh
cd /workspace/senatemovement
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python app.py
```

The server binds to 127.0.0.1:8000. Until an administrator is configured, the login screen is available but records remain inaccessible. No default credentials are provided. Stop the server and configure your own account privately when ready:

```sh
.venv/bin/python app.py --setup-admin
.venv/bin/python app.py
```

Passwords require at least 12 characters and are stored as salted PBKDF2 hashes. Never supply real login details in chat or commit them to Git.

```sh
.venv/bin/python -m unittest -v
```

## Benue South scope and data

The district covers Ado, Agatu, Apa, Obi, Ogbadibo, Ohimini, Oju, Okpokwu and Otukpo. Only these nine Benue South LGAs are accepted by forms, imports, database constraints and coordinator scopes. The bundled district directory contains **1,373 PUs in 102 wards across all nine LGAs**, extracted from the user-supplied `Nigeria_polling_units.csv`. No location fields are missing and PU codes are unique. This snapshot has not been independently verified as a current official register.

For district performance, the dashboard shows at most 50 matching polling-unit edit forms; use Find records to narrow to another PU. The records table and CSV exports retain all matching records.

Location-only seeding leaves voter totals NULL and preserves existing records, assignments, reports and sourced totals. The historical 2023 registered-voter baseline still covers only 236 Apa/Agatu PUs; the upload contains no district voter totals.

Source checksum and per-LGA counts are in `data/benue_directory_source.json`. Reproduce the extraction with:

```sh
.venv/bin/python tools/extract_benue.py /path/to/Nigeria_polling_units.csv --output /tmp/benue-extract
```

Review new source snapshots before replacing the bundled data. The old Apa/Agatu snapshot is retained solely to validate the independent historical baseline.

Administrators can add PUs or use **Import PUs** with the header:

```csv
lga,ward,code,name,voters,source,source_date
```

Imports require a sourced nonnegative voter total and ISO source date, are previewed, and reject conflicting codes atomically. Unknown values must not be guessed as zero. A directory-only district source with unknown totals needs a dedicated reviewed importer before loading. The existing baseline remains historical, separate from any new totals.

## Accounts and configuration

See [Administrator setup](ADMIN_SETUP.md) for private first login, account roles, recovery and hosted provisioning.

Roles: administrator, viewer, LGA/ward coordinator, and single-PU agent. Authentication, CSRF checks, login throttling and area authorization are inherited from the reference; there is no public signup. Accounts and login credentials are reserved for later private setup. No upstream accounts or personal data were copied.

- `SENATE_MOVEMENT_DB`: local SQLite path; defaults to `senatemovement.sqlite3`.
- `SENATE_MOVEMENT_ENV=production`: required for hosted startup and Secure cookies.
- `DATABASE_URL` and `DATABASE_URL_UNPOOLED`: optional hosted PostgreSQL configuration.
- `APP_ORIGIN`, `ADMIN_NAME`, `ADMIN_PASSWORD_HASH`: hosting configuration; see DEPLOYMENT.md.

Do not point this portal at the original portal's database. Use separate credentials and database resources. `render.yaml` prepares the new service but does not deploy it. Production PostgreSQL integration requires a separate disposable test database; local SQLite tests do not establish hosted readiness.

## Pending information

- Any additional logo or photos, reserved for the owner. The display name is Senate Movement for Olofu 2027.
- Any approved district historical voter totals; the location directory is now loaded.
- Intended administrator and account scopes, configured securely outside chat.
- Hosting service and a separate persistent database before deployment.

The layout and functional workflows follow the reference; personal branding is visibly reserved. See UPSTREAM.md for the exact source commit. Source deployment details remain in DEPLOYMENT.md with the new variable/service names.
