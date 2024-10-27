#!/bin/bash

# Exec migrations
#python manage.py migrate --noinput

# Create o superuser if no exists
echo "from django.contrib.auth import get_user_model; User = get_user_model(); \
      User.objects.filter(username='admin').exists() or \
      User.objects.create_superuser('admin', 'admin@example.com', 'adminpassword')" | python manage.py shell

# Run server
exec "$@"
