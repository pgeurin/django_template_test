# Setting Up Google OAuth for Django Template

This guide will walk you through the process of setting up Google OAuth for your Django Template project.

## Option 1: Using the Google Cloud Console (Manual Setup)

1. Go to the [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Navigate to "APIs & Services" > "OAuth consent screen"
4. Set up the OAuth consent screen:
   - User Type: External
   - App name: Django Template
   - User support email: your-email@example.com
   - Developer contact information: your-email@example.com
   - Authorized domains: Add your domain or use localhost for development
5. Add scopes:
   - .../auth/userinfo.profile
   - .../auth/userinfo.email
   - .../auth/calendar.readonly (if needed)
6. Navigate to "APIs & Services" > "Credentials"
7. Click "Create Credentials" > "OAuth client ID"
8. Select "Web application" as the application type
9. Add authorized redirect URIs:
   - http://localhost:8000/accounts/google/login/callback/
   - http://127.0.0.1:8000/accounts/google/login/callback/
10. Click "Create"
11. Note down the Client ID and Client Secret

## Option 2: Using the Provided Script (Automated Setup)

We've created a script to automate the OAuth setup process:

```bash
./setup_oauth.sh
```

This script will:
1. Create an OAuth consent screen
2. Create OAuth client credentials
3. Save the credentials to a file
4. Provide instructions for Django setup

## Setting Up in Django Admin

1. Go to http://127.0.0.1:8000/admin/
2. Log in with admin@example.com / adminpassword
3. Go to "Social Applications" under "Social Accounts"
4. Click "Add Social Application"
5. Fill in the details:
   - Provider: Google
   - Name: Google
   - Client ID: (Your Google OAuth client ID)
   - Secret key: (Your Google OAuth client secret)
   - Sites: Add your site (select "example.com" or your domain)
6. Click "Save"

## Testing Google Login

1. Go to http://127.0.0.1:8000/accounts/login/
2. Click the "Login with Google" button
3. Follow the Google OAuth flow
4. You should be redirected back to your Django site and logged in

## Troubleshooting

- If you get a redirect URI mismatch error, ensure the redirect URI in your Google Cloud Console matches exactly what Django is using
- Check that the site domain in Django admin matches the domain you're accessing the site from
- Ensure the OAuth consent screen is properly configured with the required scopes
- Verify that the Google+ API and Calendar API are enabled in your Google Cloud project
