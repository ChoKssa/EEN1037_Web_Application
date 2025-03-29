#!/bin/sh
set -ex

# Move to application directory
cd /app

# Run any new database migrations
python ./manage.py migrate

# Create Admin User, ignore errors if it already exists
python ./manage.py createsuperuser --noinput || true

# Run Django's development server
python ./manage.py runserver 0.0.0.0:8000
