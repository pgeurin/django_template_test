# Google OAuth Setup for Django on Render

This guide provides step-by-step instructions for setting up Google OAuth authentication for a Django application deployed on Render.

## 1. Google Cloud Console Setup

### Create a Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Click on the project dropdown at the top of the page
3. Click "New Project"
4. Enter a project name and click "Create"
5. Select your new project from the dropdown

### Enable APIs

1. Go to "APIs & Services" > "Library"
2. Search for "Google+ API" and enable it
3. Search for "Google Calendar API" and enable it (if needed)
4. Search for any other APIs your application requires

### Configure OAuth Consent Screen

1. Go to "APIs & Services" > "OAuth consent screen"
2. Select "External" user type and click "Create"
3. Fill in required information:
   - App name: Your application name
   - User support email: Your email address
   - Developer contact information: Your email address
4. Click "Save and Continue"
5. Add scopes:
   - email
   - profile
   - openid
   - https://www.googleapis.com/auth/calendar.readonly (if needed)
6. Click "Save and Continue"
7. Add test users (if in testing mode):
   - Enter email addresses of test users
   - Click "Save and Continue"
8. Review your settings and click "Back to Dashboard"

### Create OAuth Credentials

1. Go to "APIs & Services" > "Credentials"
2. Click "Create Credentials" > "OAuth client ID"
3. Select "Web application" as the application type
4. Name: Your application name
5. Authorized JavaScript origins:
   - `https://your-app-name.onrender.com`
6. Authorized redirect URIs:
   - `https://your-app-name.onrender.com/accounts/google/login/callback/`
7. Click "Create"
8. Note your Client ID and Client Secret

## 2. Render Configuration

### Add Environment Variables

1. Go to your web service in the [Render Dashboard](https://dashboard.render.com/)
2. Click on the "Environment" tab
3. Add the following environment variables:
   - Key: `GOOGLE_CLIENT_ID` 
     Value: Your Google OAuth client ID
   - Key: `GOOGLE_CLIENT_SECRET`
     Value: Your Google OAuth client secret
4. Click "Save Changes"

## 3. Django Configuration

### Configure django-allauth

Ensure your settings.py has the following configuration:

```python
INSTALLED_APPS = [
    # ... other apps
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
]

MIDDLEWARE = [
    # ... other middleware
    'allauth.account.middleware.AccountMiddleware',
]

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

SITE_ID = 1

# Allauth settings
ACCOUNT_EMAIL_VERIFICATION = 'none'  # Change as needed
ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = True
ACCOUNT_LOGOUT_ON_GET = True
ACCOUNT_SESSION_REMEMBER = True

# Login/logout redirect URLs
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

# Social account settings
SOCIALACCOUNT_EMAIL_REQUIRED = True
SOCIALACCOUNT_EMAIL_VERIFICATION = 'none'
SOCIALACCOUNT_QUERY_EMAIL = True
SOCIALACCOUNT_LOGIN_ON_GET = True
SOCIALACCOUNT_AUTO_SIGNUP = True

# Google OAuth settings
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': [
            'profile',
            'email',
            'openid',
            'https://www.googleapis.com/auth/calendar.readonly',  # If needed
        ],
        'AUTH_PARAMS': {
            'access_type': 'offline',
        },
        'OAUTH_PKCE_ENABLED': True,
    }
}
```

### Configure URLs

Ensure your urls.py includes allauth URLs:

```python
from django.urls import path, include

urlpatterns = [
    # ... other URL patterns
    path('accounts/', include('allauth.urls')),
]
```

## 4. Post-Deployment Setup

### Configure Social Application in Django Admin

1. Access your Django admin panel at `https://your-app-name.onrender.com/admin/`
2. Log in with your superuser credentials
3. Go to "Social Applications" under "Social Accounts"
4. Click "Add Social Application"
5. Fill in the form:
   - Provider: Google
   - Name: Google OAuth
   - Client ID: Your Google OAuth client ID
   - Secret key: Your Google OAuth client secret
   - Sites: Select your site and add it to "Chosen sites"
6. Click "Save"

## 5. Testing

1. Visit your application at `https://your-app-name.onrender.com`
2. Click on the Google login button
3. You should be redirected to Google's authentication page
4. After authenticating, you should be redirected back to your application
5. Verify that you are logged in successfully

## 6. Troubleshooting

- **Redirect URI Mismatch**: Ensure the redirect URI in Google Cloud Console matches exactly with your application's callback URL
- **Invalid Client ID**: Verify that the client ID in your Django admin matches the one in Google Cloud Console
- **Invalid Client Secret**: Verify that the client secret in your Django admin matches the one in Google Cloud Console
- **Domain Verification**: If your application is in production mode, you may need to verify your domain
- **Consent Screen Not Configured**: Ensure your OAuth consent screen is properly configured
- **API Not Enabled**: Ensure the necessary APIs are enabled in Google Cloud Console

## 7. Security Considerations

- Keep your client secret secure
- Use HTTPS for all OAuth traffic
- Regularly review authorized applications
- Implement proper CSRF protection
- Consider implementing additional security measures like two-factor authentication
