# Deploying to Render

This document provides step-by-step instructions for deploying your Django application to Render.

## Prerequisites

1. Your code has been pushed to GitHub at: https://github.com/pgeurin/django_template.git
2. You have a Render account. If not, sign up at [render.com](https://render.com)

## Deployment Steps

### 1. Sign in to Render

Go to [render.com](https://render.com) and sign in to your account.

### 2. Create a New Blueprint Instance

1. In the Render dashboard, click on the "New +" button in the top right corner
2. Select "Blueprint" from the dropdown menu
3. Connect your GitHub account if you haven't already
4. Select the repository: `pgeurin/django_template`
5. Click "Connect"

### 3. Configure and Deploy

1. Render will automatically detect the `render.yaml` file in your repository
2. Review the services that will be created:
   - Web service: django-template
   - PostgreSQL database: django-template-db
3. Click "Apply" to start the deployment process

### 4. Monitor Deployment

1. Render will create the services defined in your `render.yaml` file
2. You can monitor the build progress in the Render dashboard
3. The initial build may take a few minutes to complete

### 5. Configure Google OAuth (if using)

After deployment is complete:

1. Go to your web service in the Render dashboard
2. Click on the "Environment" tab
3. Add your Google OAuth credentials:
   - `GOOGLE_CLIENT_ID`: Your Google OAuth client ID
   - `GOOGLE_CLIENT_SECRET`: Your Google OAuth client secret
4. Make sure to update your Google OAuth authorized redirect URIs to include your Render domain:
   - `https://django-template.onrender.com/accounts/google/login/callback/`

### 6. Access Your Deployed Application

Once deployment is complete, you can access your application at:
- `https://django-template.onrender.com`

## Troubleshooting

If you encounter any issues during deployment:

1. Check the build logs in the Render dashboard
2. Verify that all environment variables are correctly set
3. Make sure your `render.yaml` file is correctly configured
4. Check that your `build.sh` script is executable and contains the correct commands

## Updating Your Application

To update your application:

1. Push changes to your GitHub repository
2. Render will automatically detect the changes and redeploy your application

## Additional Resources

- [Render Documentation](https://render.com/docs)
- [Django on Render](https://render.com/docs/deploy-django)
