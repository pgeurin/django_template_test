#!/usr/bin/env python
"""
Debug script to check OAuth configuration
"""

import os
import sys
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'heyyoufree.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
django.setup()

# Import models after Django setup
from django.contrib.sites.models import Site
from allauth.socialaccount.models import SocialApp

def debug_oauth_config():
    """Print debug information about OAuth configuration"""
    # Check site configuration
    try:
        site = Site.objects.get_current()
        print(f"Current site: id={site.id}, domain={site.domain}, name={site.name}")
    except Site.DoesNotExist:
        print("No site configured!")
    
    # Check all sites
    print("\nAll sites:")
    for s in Site.objects.all():
        print(f"- id={s.id}, domain={s.domain}, name={s.name}")
    
    # Check social apps
    print("\nSocial apps:")
    for app in SocialApp.objects.all():
        print(f"- id={app.id}, provider={app.provider}, name={app.name}")
        print(f"  client_id={app.client_id[:10]}...")
        print(f"  secret={app.secret[:5]}...")
        print(f"  sites: {', '.join(str(s.domain) for s in app.sites.all())}")
    
    # Check expected callback URLs
    print("\nExpected callback URLs:")
    for s in Site.objects.all():
        print(f"- For site {s.domain}: http://{s.domain}/accounts/google/login/callback/")
    
    # Print Django settings
    from django.conf import settings
    print("\nDjango settings:")
    print(f"- SITE_ID: {settings.SITE_ID}")
    print(f"- SOCIALACCOUNT_PROVIDERS: {settings.SOCIALACCOUNT_PROVIDERS}")

if __name__ == "__main__":
    debug_oauth_config()
