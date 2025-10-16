from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Custom User model extending Django's AbstractUser.
    Add custom fields as needed.
    """
    email = models.EmailField(unique=True)
    
    # Add custom fields here as your project grows
    # Example:
    # phone_number = models.CharField(max_length=20, blank=True)
    # bio = models.TextField(blank=True)
    
    def __str__(self):
        return self.email
