#!/bin/bash
set -e

echo "Starting Django Portfolio Application..."

# Wait for database to be ready (if using external database)
echo "Waiting for database..."
until python manage.py migrate --check 2>/dev/null; do
    echo "Database is unavailable - sleeping"
    sleep 1
done

echo "Database is up - executing commands"

# Run database migrations
echo "Running database migrations..."
python manage.py migrate --noinput

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput --clear

# Create superuser if it doesn't exist
echo "Creating superuser if needed..."
python manage.py shell << EOF
from django.contrib.auth.models import User
import os

username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin')
email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@example.com')
password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'admin123')

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username, email, password)
    print(f"Superuser '{username}' created successfully.")
else:
    print(f"Superuser '{username}' already exists.")
EOF

# Start supervisor to manage all processes
echo "Starting services with supervisor..."
exec /usr/bin/supervisord -c /etc/supervisor/conf.d/supervisord.conf