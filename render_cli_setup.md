# Render CLI Deployment Guide

This guide explains how to use the Render CLI to deploy your Django application.

## Prerequisites

1. Install the Render CLI:
   ```bash
   brew install render  # macOS
   # OR download from https://github.com/render-oss/cli/releases
   ```

2. Get your Render API key:
   - Go to https://dashboard.render.com/user/settings
   - Under "API Keys", create a new API key
   - Copy the key for use in the next step

## Authentication

Set your API key as an environment variable:

```bash
export RENDER_API_KEY=your_api_key_here
```

## Deployment Options

### Option 1: Quick Deploy (Using Existing Service)

If you already have a service set up on Render:

1. Find your service ID from the Render dashboard URL:
   - Example: https://dashboard.render.com/web/srv-XXXXXXXX
   - The service ID is the `srv-XXXXXXXX` part

2. Run the deployment script:
   ```bash
   ./deploy_to_render.sh srv-XXXXXXXX
   ```

### Option 2: Create a New Service with Blueprint

If you want to create a new service using the `render.yaml` blueprint:

1. Push your code to GitHub
2. In the Render dashboard:
   - Click "New" > "Blueprint"
   - Connect to your GitHub repository
   - Render will automatically detect the `render.yaml` file
   - Click "Apply" to create the services

3. After the service is created, you can use the deployment script for future updates.

### Option 3: Manual Service Creation via CLI

You can also create services directly with the CLI:

```bash
# List available service types
render services create --help

# Create a web service
render services create web \
  --name "django-template" \
  --repo "https://github.com/yourusername/django_template" \
  --branch main \
  --build-command "./build.sh" \
  --start-command "cd django_app && gunicorn django_template.wsgi:application" \
  --env-vars "DEBUG=False" \
  --env-vars "ALLOWED_HOSTS=.onrender.com"
```

## Common Commands

```bash
# List all services
render services

# View service details
render services get srv-XXXXXXXX

# View logs
render logs srv-XXXXXXXX

# Restart a service
render restart srv-XXXXXXXX

# Create a manual deployment
render deploys create srv-XXXXXXXX

# List deployments for a service
render deploys list srv-XXXXXXXX
```

## Environment Variables

To set environment variables for your service:

```bash
render services env-vars set srv-XXXXXXXX \
  --key SECRET_KEY --value "your-secret-key" \
  --key DEBUG --value "False"
```

## Database Access

To access your PostgreSQL database:

```bash
# Find your database ID
render services

# Connect using psql
render psql pgsql-XXXXXXXX
```
