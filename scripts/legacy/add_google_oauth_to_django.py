#!/usr/bin/env python
"""
Script to add Google OAuth credentials directly to Django database.
Usage: python add_google_oauth_to_django.py <client_id> <client_secret>
"""

import os
import sys
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_template.settings')
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'django_app'))
django.setup()

# Import models after Django setup
from django.contrib.sites.models import Site
from allauth.socialaccount.models import SocialApp

def add_google_oauth(client_id, client_secret):
    """Add Google OAuth credentials to Django database."""
    # Get the default site
    site = Site.objects.get_current()
    
    # Check if a Google SocialApp already exists
    try:
        app = SocialApp.objects.get(provider='google')
        print(f"Updating existing Google OAuth app (ID: {app.id})")
    except SocialApp.DoesNotExist:
        app = SocialApp(provider='google', name='Google')
        print("Creating new Google OAuth app")
    
    # Update the credentials
    app.client_id = client_id
    app.secret = client_secret
    app.save()
    
    # Make sure the app is associated with the site
    app.sites.add(site)
    
    print(f"Successfully added Google OAuth credentials for site: {site.domain}")
    print(f"Client ID: {client_id}")
    print(f"Client Secret: {client_secret[:5]}...{client_secret[-5:]} (masked for security)")

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python add_google_oauth_to_django.py <client_id> <client_secret>")
        sys.exit(1)
    
    client_id = sys.argv[1]
    client_secret = sys.argv[2]
    
    add_google_oauth(client_id, client_secret)
