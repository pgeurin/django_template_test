# Django Deployment Runbook for Render

This runbook provides step-by-step instructions for deploying a Django application on Render with Google OAuth authentication.

**⚠️ IMPORTANT LESSONS LEARNED:**
This runbook has been updated based on real deployment experience. The original runbook was missing critical steps that caused 500 errors and deployment failures.

## Prerequisites

- GitHub repository with Django project
- Google Cloud Platform account
- Render account
- Django project with Google OAuth integration (using django-allauth)

## 1. Prepare Your Django Project

### 1.1. Configure Environment Variables

Ensure your Django settings.py uses environment variables for sensitive information:
```python
# settings.py
import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY', 'default-secret-key-for-dev')
DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')
```

### 1.2. Configure Database Settings

Ensure your database settings support PostgreSQL with dj-database-url:
```python
# settings.py
import dj_database_url

# Database configuration
if os.getenv('DATABASE_URL'):
    # Parse DATABASE_URL (used by Render)
    DATABASES = {
        'default': dj_database_url.parse(os.getenv('DATABASE_URL'))
    }
else:
    # Fallback to SQLite for development
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
```

### 1.3. Configure Static Files

Set up WhiteNoise for static file handling:
```python
# settings.py
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Add this line
    # other middleware...
]

STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
```

### 1.4. Configure Google OAuth in Settings

**CRITICAL:** Configure Google OAuth to use environment variables instead of database:

```python
# settings.py
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': [
            'profile',
            'email',
            'openid',
        ],
        'AUTH_PARAMS': {
            'access_type': 'offline',
        },
        'OAUTH_PKCE_ENABLED': True,
        'APP': {
            'client_id': os.getenv('GOOGLE_CLIENT_ID'),
            'secret': os.getenv('GOOGLE_CLIENT_SECRET'),
        }
    }
}
```

**⚠️ LESSON LEARNED:** The original configuration used database SocialApp records, which caused 500 errors because the OAuth credentials weren't configured in the database for the new service.

### 1.5. Create Build Script

Create a build.sh file in your project root:
```bash
#!/usr/bin/env bash
# exit on error
set -o errexit

# Install dependencies
pip install -r requirements.prod.txt

# Collect static files
python django_app/manage.py collectstatic --no-input

# Run migrations
python django_app/manage.py migrate
```

Make it executable:
```bash
chmod +x build.sh
```

### 1.6. Create render.yaml

Create a render.yaml file in your project root:
```yaml
services:
  - type: web
    name: django-template
    runtime: python
    buildCommand: |
      pip install -r requirements.txt
      cd django_app && python manage.py migrate
      cd django_app && python manage.py shell -c "
      from django.contrib.auth import get_user_model;
      User = get_user_model();
      if not User.objects.filter(is_superuser=True).exists():
          User.objects.create_superuser('admin', 'admin@example.com', 'admin123');
          print('Superuser created')
      else:
          print('Superuser exists')
      "
    startCommand: cd django_app && gunicorn django_template.wsgi:application
    envVars:
      - key: DEBUG
        value: False
      - key: SECRET_KEY
        generateValue: true
      - key: ALLOWED_HOSTS
        value: "django-template.onrender.com,.onrender.com"
      - key: DATABASE_URL
        fromDatabase:
          name: django-template-db
          property: connectionString
      - key: PYTHON_VERSION
        value: 3.11.0

databases:
  - name: django-template-db
    databaseName: django_template
    user: django_template
    plan: free
```

**⚠️ CRITICAL LESSONS LEARNED:**
1. **Database Migrations**: Must be run during build, not just at startup
2. **Superuser Creation**: Must be automated during deployment
3. **ALLOWED_HOSTS**: Must include the exact Render domain
4. **Build Command**: Must use multi-line format for complex commands

> **Important**: Make sure gunicorn is included in your requirements.txt file to avoid the "gunicorn: command not found" error. Render uses separate environments for build and runtime, so dependencies must be in requirements.txt to be available at runtime.

### 1.6. Update requirements.prod.txt

Ensure your production requirements include gunicorn:
```
# Production requirements
-r requirements.txt

# Production server
gunicorn==21.2.0
```

## 2. Set Up Google OAuth

### 2.1. Create Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the Google+ API and Google Calendar API (if needed)

### 2.2. Configure OAuth Consent Screen

1. Go to "APIs & Services" > "OAuth consent screen"
2. Select "External" user type
3. Fill in required information:
   - App name
   - User support email
   - Developer contact information
4. Add scopes: email, profile, openid
5. Add test users if in testing mode

### 2.3. Create OAuth Credentials

1. Go to "APIs & Services" > "Credentials"
2. Click "Create Credentials" > "OAuth client ID"
3. Select "Web application" as the application type
4. Add a name for your OAuth client
5. Add authorized JavaScript origins:
   - `https://your-app-name.onrender.com`
6. Add authorized redirect URIs:
   - `https://your-app-name.onrender.com/accounts/google/login/callback/`
7. Click "Create" and note your Client ID and Client Secret

## 3. Deploy to Render

### 3.1. Push to GitHub

Commit and push all changes to GitHub:
```bash
git add .
git commit -m "Prepare for Render deployment"
git push origin main
```

### 3.2. Create Render Blueprint

1. Log in to [Render Dashboard](https://dashboard.render.com/)
2. Click "New" > "Blueprint"
3. Connect your GitHub repository
4. Render will automatically detect the render.yaml file
5. Click "Apply" to create the services defined in render.yaml

### 3.3. Configure Google OAuth in Render

**⚠️ CRITICAL STEP:** This step is essential to prevent 500 errors on login pages.

1. After services are created, go to your web service in the Render dashboard
2. Click on "Environment" tab
3. Add the following environment variables:
   - `GOOGLE_CLIENT_ID`: Your Google OAuth client ID
   - `GOOGLE_CLIENT_SECRET`: Your Google OAuth client secret

**⚠️ LESSON LEARNED:** Without these environment variables, the login pages will return 500 errors because Django-allauth cannot find the Google OAuth credentials.

### 3.4. Set Up Google OAuth in Django Admin

1. After deployment, access your Django admin panel at:
   - `https://your-app-name.onrender.com/admin/`
2. Log in with your superuser credentials
3. Go to "Social Applications" under "Social Accounts"
4. Add a new social application:
   - Provider: Google
   - Name: Google OAuth
   - Client ID: Your Google OAuth client ID
   - Secret key: Your Google OAuth client secret
   - Sites: Select your site and add it to "Chosen sites"

## 4. Monitor and Verify Deployment

### 4.1. Monitor Deployment Progress

1. Deployments on Render can take 5-15 minutes to complete, especially for the first deployment
2. You can monitor the deployment status using the Render CLI:
   ```bash
   export RENDER_API_KEY=your_render_api_key
   render deploys list your_service_id --output text
   ```
3. Check deployment logs for progress and potential issues:
   ```bash
   render logs -r your_service_id --output text
   ```
4. Common deployment states:
   - `Created`: Deployment has been created but not yet started
   - `Build In Progress`: Building the application
   - `Live`: Successfully deployed and running
   - `Update Failed`: Deployment failed (check logs for errors)

### 4.2. Test the Application

1. Once the deployment shows as `Live`, visit your application at `https://your-app-name.onrender.com`
2. Test the Google login functionality
3. Verify that all features are working correctly

### 4.2. Monitor Logs

Check logs for any errors:
```bash
export RENDER_API_KEY=your_render_api_key
render logs -r your_service_id --output text
```

### 4.3. Check Database Connection

Verify database connectivity:
```bash
export RENDER_API_KEY=your_render_api_key
render psql your_database_id
```

## 5. Maintenance and Updates

### 5.1. Update Application

1. Make changes to your code
2. Commit and push to GitHub
3. Render will automatically deploy the changes if auto-deploy is enabled

### 5.2. Manual Deployment

If needed, trigger a manual deployment:
```bash
export RENDER_API_KEY=your_render_api_key
render deploys create your_service_id --confirm --output text
```

### 5.3. Scale Application

If needed, upgrade your plan in the Render dashboard to handle more traffic.

## 6. Troubleshooting

### 6.1. Common Issues

- **Static Files Not Loading**: Check STATIC_ROOT and STATICFILES_STORAGE settings
- **Database Connection Errors**: Verify DATABASE_URL environment variable
- **Google OAuth Not Working**: Check redirect URIs and credentials
- **500 Server Errors**: Check application logs for details
- **"gunicorn: command not found"**: Make sure gunicorn is included in your requirements.txt file:
  ```bash
  # Add to requirements.txt
  gunicorn==21.2.0
  ```
  Remember that Render uses separate environments for build and runtime, so dependencies must be in requirements.txt to be available at runtime.

### 6.2. Critical Issues Discovered During Real Deployment

**🚨 500 Error on Login Pages**
- **Cause**: Google OAuth credentials not configured in environment variables
- **Solution**: Set `GOOGLE_CLIENT_ID` and `GOOGLE_CLIENT_SECRET` in Render dashboard
- **Prevention**: Configure Google OAuth to use environment variables in settings.py

**🚨 Database Migrations Not Run**
- **Cause**: Migrations only run at startup, not during build
- **Solution**: Add `python manage.py migrate` to buildCommand in render.yaml
- **Prevention**: Always run migrations during build phase

**🚨 No Superuser Created**
- **Cause**: No automated superuser creation during deployment
- **Solution**: Add superuser creation to buildCommand in render.yaml
- **Prevention**: Automate superuser creation in deployment process

**🚨 ALLOWED_HOSTS Configuration**
- **Cause**: ALLOWED_HOSTS not configured for exact Render domain
- **Solution**: Set ALLOWED_HOSTS to include exact domain: `"your-app.onrender.com,.onrender.com"`
- **Prevention**: Always include exact domain in ALLOWED_HOSTS

**🚨 Build Command Failures**
- **Cause**: Complex build commands not properly formatted
- **Solution**: Use multi-line YAML format with `|` for buildCommand
- **Prevention**: Test build commands locally before deployment

### 6.2. Render Support

If you encounter issues specific to Render, consult their documentation or contact support:
- [Render Documentation](https://render.com/docs)
- [Render Support](https://render.com/support)

## 7. Security Considerations

- Keep your SECRET_KEY secure and unique for each environment
- Use HTTPS for all production traffic
- Regularly update dependencies to patch security vulnerabilities
- Implement proper authentication and authorization
- Set up proper CORS settings for API endpoints

## 8. Backup and Recovery

- Regularly backup your database
- Document the recovery process
- Test the recovery process periodically

## 7. Complete Deployment Checklist

### Pre-Deployment Checklist
- [ ] Django settings configured for environment variables
- [ ] Google OAuth configured to use environment variables (not database)
- [ ] Database settings support PostgreSQL with dj-database-url
- [ ] Static files configured with WhiteNoise
- [ ] render.yaml created with proper buildCommand including migrations and superuser creation
- [ ] requirements.txt includes gunicorn
- [ ] ALLOWED_HOSTS includes exact Render domain

### Deployment Checklist
- [ ] GitHub repository created and code pushed
- [ ] Render Blueprint created and applied
- [ ] Google OAuth environment variables set in Render dashboard:
  - [ ] `GOOGLE_CLIENT_ID`
  - [ ] `GOOGLE_CLIENT_SECRET`
- [ ] Google Cloud Console redirect URI updated
- [ ] Deployment completed successfully (status: Live)
- [ ] Database migrations run during build
- [ ] Superuser created during build

### Post-Deployment Verification
- [ ] Homepage loads correctly
- [ ] Login page loads without 500 errors
- [ ] Google OAuth login redirects properly
- [ ] Admin panel accessible
- [ ] API endpoints working
- [ ] All tests pass

### Critical Success Factors
1. **Environment Variables**: Google OAuth credentials must be set in Render dashboard
2. **Database Setup**: Migrations must run during build phase
3. **Superuser Creation**: Must be automated in build process
4. **Domain Configuration**: ALLOWED_HOSTS must include exact Render domain
5. **Build Process**: Complex commands must use proper YAML formatting

---

This runbook provides a comprehensive guide for deploying a Django application with Google OAuth on Render. This version has been updated based on real deployment experience and includes all critical steps that were missing from the original runbook.
