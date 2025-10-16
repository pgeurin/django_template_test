#!/usr/bin/env python
import os
import django
from django.core.management import execute_from_command_line

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_template_test.settings')
django.setup()

# Create superuser
from django.contrib.auth import get_user_model
User = get_user_model()

# Check if superuser already exists
if not User.objects.filter(is_superuser=True).exists():
    User.objects.create_superuser(
        username='admin',
        email='admin@example.com',
        password='admin123'
    )
    print("Superuser created: admin/admin123")
else:
    print("Superuser already exists")
