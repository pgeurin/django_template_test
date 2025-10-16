#!/usr/bin/env bash
# exit on error
set -o errexit

# Install dependencies
pip install -r requirements.txt
pip install gunicorn==21.2.0

# Collect static files
python django_app/manage.py collectstatic --no-input

# Run migrations
python django_app/manage.py migrate
