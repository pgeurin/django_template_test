# Manual Google OAuth Setup for Django Template

## Step 1: Create a Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Click on "Select a project" at the top of the page
3. Click "New Project"
4. Enter "Django Template" as the project name
5. Click "Create"

## Step 2: Configure the OAuth Consent Screen

1. Select your new project
2. Go to "APIs & Services" > "OAuth consent screen"
3. Select "External" for User Type
4. Click "Create"
5. Fill in the required fields:
   - App name: Django Template
   - User support email: your-email@example.com
   - Developer contact information: your-email@example.com
6. Click "Save and Continue"
7. Add scopes:
   - Click "Add or Remove Scopes"
   - Select:
     - ./auth/userinfo.profile
     - ./auth/userinfo.email
     - ./auth/calendar.readonly (if needed)
   - Click "Update"
8. Click "Save and Continue"
9. Skip the "Test users" section by clicking "Save and Continue"
10. Review your settings and click "Back to Dashboard"

## Step 3: Create OAuth Client ID

1. Go to "APIs & Services" > "Credentials"
2. Click "Create Credentials" > "OAuth client ID"
3. Select "Web application" as the application type
4. Name: "Django Template Web Client"
5. Add Authorized JavaScript origins:
   - http://localhost:8000
   - http://127.0.0.1:8000
6. Add Authorized redirect URIs:
   - http://localhost:8000/accounts/google/login/callback/
   - http://127.0.0.1:8000/accounts/google/login/callback/
7. Click "Create"
8. A popup will show your Client ID and Client Secret - copy these values

## Step 4: Enable Required APIs

1. Go to "APIs & Services" > "Library"
2. Search for and enable these APIs:
   - Google+ API
   - Google Calendar API
   - People API

## Step 5: Configure Django

1. Go to http://127.0.0.1:8000/admin/
2. Log in with admin@example.com / adminpassword
3. Go to "Social Applications" under "Social Accounts"
4. Click "Add Social Application"
5. Fill in the details:
   - Provider: Google
   - Name: Google
   - Client ID: (Your Google OAuth client ID from step 3)
   - Secret key: (Your Google OAuth client secret from step 3)
   - Sites: Add your site (select "example.com" or your domain)
6. Click "Save"

## Step 6: Test Google Login

1. Go to http://127.0.0.1:8000/accounts/login/
2. Click the "Login with Google" button
3. You should be redirected to Google's OAuth consent screen
4. After granting permission, you should be redirected back to your Django site and logged in

## Troubleshooting

- If you get a "redirect_uri_mismatch" error, double-check that the redirect URI in your Google Cloud Console matches exactly what Django is using
- Ensure the site domain in Django admin matches the domain you're accessing the site from
- If you get a "This app isn't verified" warning, you can proceed by clicking "Advanced" and then "Go to Django Template (unsafe)"
- For development purposes, you can add yourself as a test user in the OAuth consent screen settings
