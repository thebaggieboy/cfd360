#!/bin/bash

# Make database directory
mkdir -p /app/data

# Apply database migrations
echo "Applying database migrations..."
python manage.py migrate

# Start server on the port specified by Render
echo "Starting server on port $PORT..."
gunicorn cfd360.wsgi:application --bind 0.0.0.0:$PORT --workers 4