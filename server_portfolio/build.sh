#!/usr/bin/env bash
# Exit on error
set -o errexit

# install requirements
echo "Installing requirements..."
pip install -r requirements.txt

# convert static assets files
echo "Collecting static files..."
python manage.py collectstatic --no-input

# apply migrations
echo "Applying migrations..."
python manage.py migrate 


