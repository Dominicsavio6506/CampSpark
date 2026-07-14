#!/usr/bin/env bash
# start.sh — Render Start Command
# Runs in the live container where the database IS reachable.

set -o errexit

echo "=== Running database migrations ==="
python manage.py migrate --no-input

echo "=== Seeding production data ==="
python seed_prod_data.py

echo "=== Starting Gunicorn ==="
exec gunicorn campspark.wsgi:application --bind 0.0.0.0:$PORT
