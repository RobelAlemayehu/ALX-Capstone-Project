#!/usr/bin/env python
"""Script to create a Django superuser non-interactively."""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fitness_tracker.settings')
django.setup()

from django.contrib.auth.models import User

# Default credentials
username = 'admin'
email = 'admin@example.com'
password = 'admin123'

# Check if superuser already exists
if User.objects.filter(username=username).exists():
    print(f"Superuser '{username}' already exists!")
    print(f"Username: {username}")
    print(f"Password: {password}")
else:
    User.objects.create_superuser(username=username, email=email, password=password)
    print("Superuser created successfully!")
    print(f"Username: {username}")
    print(f"Password: {password}")
    print("\nYou can now login to the admin panel at: http://localhost:8000/admin/")


