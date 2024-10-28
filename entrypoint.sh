#!/bin/sh
# entrypoint.sh

# Aplica as migrações
python manage.py makemigrations
python manage.py migrate

# Cria o superusuário automaticamente, se precisar
python manage.py shell <<EOF
from django.contrib.auth import get_user_model
User = get_user_model()
username = "admin"
email = "admin@example.com"
password = "adminpassword"
if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username=username, email=email, password=password)
EOF

