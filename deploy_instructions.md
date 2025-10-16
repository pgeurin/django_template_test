# Deployment Instructions

## Option 1: Deploy via Render Dashboard (Recommended)

1. **Push your code to GitHub**
   - Make sure all your changes are committed and pushed to GitHub

2. **Create a new Blueprint in Render**
   - Go to [Render Dashboard](https://dashboard.render.com/)
   - Click on "New" and select "Blueprint"
   - Connect your GitHub repository
   - Render will automatically detect the `render.yaml` file
   - Review the services that will be created:
     - Web service: django-template
     - PostgreSQL database: django-template-db
   - Click "Apply" to start the deployment process

3. **Monitor the deployment**
   - Render will create the services defined in your `render.yaml` file
   - You can monitor the build progress in the Render dashboard
   - The initial build may take a few minutes to complete

4. **Configure Google OAuth (if using)**
   - Go to your web service in the Render dashboard
   - Click on the "Environment" tab
   - Add your Google OAuth credentials:
     - `GOOGLE_CLIENT_ID`: Your Google OAuth client ID
     - `GOOGLE_CLIENT_SECRET`: Your Google OAuth client secret
   - Update your Google OAuth authorized redirect URIs to include your Render domain:
     - `https://django-template.onrender.com/accounts/google/login/callback/`

## Option 2: Deploy via Render Deploy Hook

Render provides deploy hooks that allow you to trigger deployments via a simple HTTP request.

1. **Get your deploy hook URL**
   - Go to your service in the Render dashboard
   - Click on "Settings"
   - Scroll down to "Deploy Hooks"
   - Create a new deploy hook and copy the URL

2. **Trigger a deployment**
   - Use curl to trigger a deployment:
   ```bash
   curl https://api.render.com/deploy/srv-XXXXX?key=YYYYY
   ```

## Option 3: Manual Deployment via GitHub Actions

Your repository is already configured with a GitHub Actions workflow that will deploy to Render when you push to the main branch.

1. **Set up GitHub repository secrets**
   - Go to your GitHub repository → Settings → Secrets and variables → Actions
   - Add two repository secrets:
     - `RENDER_SERVICE_ID`: Your Render service ID (format: srv-XXXXXXXX)
     - `RENDER_API_KEY`: Your Render API key (from Render dashboard)

2. **Push to main branch**
   - The GitHub Actions workflow will automatically run when you push to the main branch
   - It will run tests and then deploy to Render

## Accessing Your Deployed Application

Once deployment is complete, you can access your application at:
- `https://django-template.onrender.com` (or the custom URL you configured)

## Troubleshooting

If you encounter any issues during deployment:

1. Check the build logs in the Render dashboard
2. Verify that all environment variables are correctly set
3. Make sure your `render.yaml` file is correctly configured
4. Check that your `build.sh` script is executable and contains the correct commands
