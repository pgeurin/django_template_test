#!/usr/bin/env python
"""
Production setup script for Django template
"""
import os
import django
from django.core.management import execute_from_command_line

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_template_test.settings')
django.setup()

def run_migrations():
    """Run database migrations"""
    print("Running database migrations...")
    execute_from_command_line(['manage.py', 'migrate'])

def create_superuser():
    """Create a superuser if one doesn't exist"""
    from django.contrib.auth import get_user_model
    User = get_user_model()
    
    if not User.objects.filter(is_superuser=True).exists():
        User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='admin123'
        )
        print("Superuser created: admin/admin123")
    else:
        print("Superuser already exists")

def setup_google_oauth():
    """Set up Google OAuth in the database"""
    from allauth.socialaccount.models import SocialApp
    from django.contrib.sites.models import Site
    
    # Get or create the site
    site, created = Site.objects.get_or_create(
        domain='django-template-test.onrender.com',
        defaults={'name': 'Django Template Test'}
    )
    
    # Get or create Google OAuth app
    google_app, created = SocialApp.objects.get_or_create(
        provider='google',
        defaults={
            'name': 'Google OAuth',
            'client_id': os.getenv('GOOGLE_CLIENT_ID', ''),
            'secret': os.getenv('GOOGLE_CLIENT_SECRET', ''),
        }
    )
    
    if created:
        print("Google OAuth app created")
    else:
        # Update existing app with environment variables
        google_app.client_id = os.getenv('GOOGLE_CLIENT_ID', '')
        google_app.secret = os.getenv('GOOGLE_CLIENT_SECRET', '')
        google_app.save()
        print("Google OAuth app updated")
    
    # Add site to the app
    google_app.sites.add(site)
    print("Google OAuth configured for site:", site.domain)

if __name__ == '__main__':
    try:
        run_migrations()
        create_superuser()
        setup_google_oauth()
        print("Production setup completed successfully!")
    except Exception as e:
        print(f"Error during setup: {e}")
        import traceback
        traceback.print_exc()
