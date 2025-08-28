#!/usr/bin/env bash
# Apply database migrations
echo "=== APPLYING DATABASE MIGRATIONS ==="
python manage.py migrate --noinput

# Create superuser automatically
echo "=== CREATING SUPERUSER ==="
python manage.py createsu

# Collect static files
echo "=== COLLECTING STATIC FILES ==="
python manage.py collectstatic --noinput --clear

echo "=== BUILD PROCESS COMPLETED ==="