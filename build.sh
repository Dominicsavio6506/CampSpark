#!/usr/bin/env bash
# build.sh — Render Build Command
# This runs in the build sandbox where external DB connections may fail.
# Only install dependencies and collect static files here.

set -o errexit

pip install -r requirements.txt

# Collect static files (whitenoise serves them in production)
python manage.py collectstatic --no-input

# Migrations and seeding run at startup, NOT during build,
# because the build sandbox cannot reach the external Postgres host.
