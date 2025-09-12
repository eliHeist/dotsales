#!/bin/bash

# Exit if any command fails
set -e

# Run migrations
python manage.py migrate

# Collect static files
# python manage.py collectstatic --noinput

# Optional: Your custom setup
# python manage.py datasetup

# Create superuser if not exists
echo "Creating default superuser (test@example.com)..."
python manage.py shell <<EOF
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.exists():
    User.objects.create_superuser(email='test@example.com', password='1234Password')
EOF

# Start Gunicorn server
exec gunicorn dotsales.wsgi:application --bind 0.0.0.0:8000 --timeout 320