#!/bin/sh


set -e

echo "Applying database migrations..."
python manage.py migrate --noinput

echo "Starting Gunicorn server..."
exec gunicorn webapp.wsgi:application --bind 0.0.0.0:8000 --workers=3 --timeout=120
