# Database installation

These scripts install the MariaDB database used by Find_a_job. `schema.sql` is the original structure exported from MariaDB 10.11.14, containing 23 tables without data. Target MariaDB 10.11 or a compatible newer version. This is not a portable SQLite or MySQL dump.

## Files

- `install.bash`: interactive installer.
- `create.sql`: creates database `job_ads_crm` with `utf8mb4_unicode_ci`.
- `schema.sql`: original table definitions, including indexes and foreign keys.
- `migration_history.sql`: migration records exported from the source database (included).

## Refresh Django migration history on the source machine

The included `migration_history.sql` restores the migration records into the empty `django_migrations` table created by the schema. Keep this file with the installer. To refresh it after further schema changes, export it again from the same source database and refresh `schema.sql` as well:

```bash
cd /home/pterik/PycharmProjects/job_ads_crm
mariadb-dump -h localhost -u job_ads_user -p \
  --no-create-info --skip-triggers --skip-add-locks --skip-disable-keys \
  --complete-insert job_ads_crm django_migrations > database/migration_history.sql
```

Adjust source host and user if necessary. Place this file next to `install.bash` before running the installer on the destination. Use source code matching the schema and history. Do not use `migrate --fake` blindly as a substitute for the missing history.

## Installation on a new database server

A running MariaDB server and a MariaDB command-line client are required. Install the client on Ubuntu if needed:

```bash
sudo apt install mariadb-client
```

From the project root:

```bash
bash database/install.bash
```

Before making any changes, the installer displays a clean-installation notice and asks once: `Continue with clean installation? [y/N]`. Enter `y` to proceed; Enter or any other answer cancels without changes. Both `schema.sql` and `migration_history.sql` are then imported automatically. All three SQL files are required. The installer never clears an existing database; it stops if tables are already present.

It then asks for the database server host, port, administrator username/password, and application username, account host, and password. The default application account is `job_ads_user` at `localhost`.

The account host identifies where Django connects FROM; the first host identifies the database server. If both run on one machine, use `localhost` for both.

The administrator needs permission to create databases and accounts and grant privileges. For Ubuntu/MariaDB root socket authentication, use `sudo bash database/install.bash`, select `localhost` and `root`, and leave the administrator password empty. Run Django commands afterwards as your regular user.

The installer refuses to import into a database that already contains tables. It creates the database and application account, grants privileges only on `job_ads_crm` (including schema changes for migrations), imports `schema.sql`, and imports `migration_history.sql` afterwards. Existing account passwords are preserved.

Passwords are entered without terminal echo, kept in private temporary files, and removed on exit. They are not passed as command-line arguments or saved in project files. Do not run with shell tracing enabled.

DDL operations are not transactional as a group. A failed import may leave some objects created. Inspect the error and database before retrying; the installer never deletes partially imported tables.

## Configure Django

Set destination connection values in the project `.env`:

```dotenv
DB_NAME=job_ads_crm
DB_USER=job_ads_user
DB_PASSWORD=your-application-password
DB_HOST=localhost
DB_PORT=3306
```

Quote and escape special characters according to python-dotenv syntax. If the account existed already, use its existing password.

After restoring migration history:

```bash
source .venv/bin/activate
python manage.py migrate
python manage.py createsuperuser
python manage.py check
```

Both schema and migration history are imported by the installer. Keep their versions synchronized with the project migration files.

The schema contains no business data, Django users, countries, technologies, CV profiles, or job boards. Data migrations already recorded as applied will not run again. Populate required reference data using Django Admin or a separate reviewed export. Pending migrations may populate data according to their code.

The existing source database on VESTA does not need installation. These scripts deploy its structure to a new empty database.
