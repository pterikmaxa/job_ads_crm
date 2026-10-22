#!/usr/bin/env bash
set +x
set -euo pipefail
umask 077

script_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
if command -v mariadb >/dev/null 2>&1; then
    db_client=mariadb
elif command -v mysql >/dev/null 2>&1; then
    db_client=mysql
else
    printf 'MySQL client not found. Install it with: sudo apt install default-mysql-client\n' >&2
    exit 1
fi
[[ -r "$script_dir/create.sql" && -r "$script_dir/schema.sql" && -r "$script_dir/migration_history.sql" ]] || {
    printf 'Missing create.sql, schema.sql, or migration_history.sql in %s\n' "$script_dir" >&2
    exit 1
}

printf 'This installer creates job_ads_crm in a new or empty database.\n'
printf 'schema.sql and migration_history.sql will be imported automatically.\n'
printf 'Installation stops if the database already contains tables.\n'
read -r -p 'Continue with clean installation? [y/N]: ' confirmation
case "$confirmation" in
    [Yy]|[Yy][Ee][Ss]) ;;
    *) printf 'Installation cancelled. Nothing was changed.\n'; exit 0 ;;
esac

read -r -p 'Database server host [localhost]: ' db_host
db_host="${db_host:-localhost}"
read -r -p 'Database server port [3306]: ' db_port
db_port="${db_port:-3306}"
[[ "$db_port" =~ ^[0-9]{1,5}$ ]] && (( 10#$db_port >= 1 && 10#$db_port <= 65535 )) || {
    printf 'Invalid port.\n' >&2
    exit 1
}
read -r -p 'Administrator username [root]: ' admin_user
admin_user="${admin_user:-root}"
read -r -s -p 'Administrator password (empty for socket authentication): ' admin_password
printf '\n'

read -r -p 'Application username [job_ads_user]: ' app_user
app_user="${app_user:-job_ads_user}"
[[ "$app_user" =~ ^[a-zA-Z0-9_]{1,32}$ ]] || {
    printf 'Application username must contain 1–32 letters, digits, or underscores.\n' >&2
    exit 1
}
read -r -p 'Application account host [localhost]: ' app_host
app_host="${app_host:-localhost}"
printf 'Account host is where Django connects FROM, not the database server address.\n'
read -r -s -p 'Application password: ' app_password
printf '\n'
read -r -s -p 'Confirm application password: ' app_password_confirm
printf '\n'
[[ -n "$app_password" && "$app_password" == "$app_password_confirm" ]] || {
    printf 'Application passwords must be nonempty and match.\n' >&2
    exit 1
}

task_tmpdir="$(mktemp -d)"
cleanup() { rm -rf -- "$task_tmpdir"; }
trap cleanup EXIT
trap 'exit 130' INT
trap 'exit 143' TERM

# Escape values for a MySQL option file, not for shell evaluation.
option_value() {
    local value="$1"
    value="${value//\\/\\\\}"
    value="${value//\"/\\\"}"
    value="${value//$'\r'/\\r}"
    value="${value//$'\t'/\\t}"
    printf '"%s"' "$value"
}

{
    printf '[client]\nhost='
    option_value "$db_host"
    printf '\nport=%s\nuser=' "$db_port"
    option_value "$admin_user"
    printf '\npassword='
    option_value "$admin_password"
    printf '\ndefault-character-set=utf8mb4\n'
} > "$task_tmpdir/client.cnf"
unset admin_password app_password_confirm

printf 'Checking administrator connection...\n'
"$db_client" --defaults-file="$task_tmpdir/client.cnf" --batch --skip-column-names \
    --execute='SELECT VERSION();'

table_count="$("$db_client" --defaults-file="$task_tmpdir/client.cnf" --batch --skip-column-names \
    --execute="SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'job_ads_crm';")"
[[ "$table_count" == 0 ]] || {
    printf 'Database job_ads_crm already contains tables. Nothing was changed.\n' >&2
    exit 1
}


# SQL literals use doubled single quotes with NO_BACKSLASH_ESCAPES enabled.
sql_literal() {
    local value="$1"
    value="${value//\'/\'\'}"
    printf "'%s'" "$value"
}

{
    printf "SET SESSION sql_mode = 'NO_BACKSLASH_ESCAPES';\n"
    cat -- "$script_dir/create.sql"
    printf '\nCREATE USER IF NOT EXISTS '
    sql_literal "$app_user"
    printf '@'
    sql_literal "$app_host"
    printf ' IDENTIFIED BY '
    sql_literal "$app_password"
    printf ';\nGRANT ALL PRIVILEGES ON `job_ads_crm`.* TO '
    sql_literal "$app_user"
    printf '@'
    sql_literal "$app_host"
    printf ';\n'
} > "$task_tmpdir/install.sql"
unset app_password

"$db_client" --defaults-file="$task_tmpdir/client.cnf" < "$task_tmpdir/install.sql"
printf 'Importing schema.sql...\n'
"$db_client" --defaults-file="$task_tmpdir/client.cnf" --database=job_ads_crm < "$script_dir/schema.sql"
printf 'Importing migration_history.sql...\n'
"$db_client" --defaults-file="$task_tmpdir/client.cnf" --database=job_ads_crm < "$script_dir/migration_history.sql"
printf 'Django migration history restored.\n'

printf '\nDatabase job_ads_crm is ready. Account: %s@%s\n' "$app_user" "$app_host"
printf 'Existing accounts keep their current passwords. Existing data is preserved.\n'
printf 'Set DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, and DB_PORT in the project .env.\n'
printf 'Follow database/README.md for Django configuration and migration history.\n'
