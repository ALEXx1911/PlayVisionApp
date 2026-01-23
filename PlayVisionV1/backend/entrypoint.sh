#!/bin/sh

set -e

# Wait for PostgreSQL to be ready
while ! pg_isready -h "${POSTGRES_HOST:-db}" -p "${POSTGRES_PORT:-5432}" -U "${POSTGRES_USER:-postgres}" > /dev/null 2>&1; do
  echo "Waiting for Postgres to be ready..."
  sleep 2
done

echo "PostgreSQL is ready!"

python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --noinput

if [ "$SEED_DB" = "true" ]; then
  python manage.py seed
fi

python -m gunicorn --config gunicorn_config.py config.wsgi:application --bind 0.0.0.0:8000