# Django on Render Deployment Checklist

## Pre-Deployment

- [ ] Django project uses environment variables for configuration
- [ ] Database settings support PostgreSQL with dj-database-url
- [ ] Static files configured with WhiteNoise
- [ ] build.sh script created and made executable
- [ ] render.yaml file created with correct configuration
- [ ] requirements.prod.txt includes gunicorn
- [ ] Google Cloud project created
- [ ] OAuth consent screen configured
- [ ] OAuth credentials created with correct redirect URIs
- [ ] All changes committed and pushed to GitHub

## Deployment

- [ ] Log in to Render Dashboard
- [ ] Create new Blueprint pointing to GitHub repository
- [ ] Apply Blueprint to create services
- [ ] Add Google OAuth environment variables
- [ ] Monitor deployment progress (can take 5-15 minutes)
  - [ ] Check deployment status using Render CLI
  - [ ] Review logs for any build or startup errors
  - [ ] Verify gunicorn is properly installed
- [ ] Wait for initial deployment to complete (status: Live)
- [ ] Access Django admin panel
- [ ] Configure Social Application for Google OAuth
- [ ] Test Google login functionality

## Post-Deployment

- [ ] Verify all features are working correctly
- [ ] Check logs for any errors
- [ ] Verify database connectivity
- [ ] Update documentation with deployment URL
- [ ] Set up monitoring (optional)
- [ ] Configure custom domain (optional)
- [ ] Set up SSL certificate (optional)

## Render CLI Commands

```bash
# Set API key
export RENDER_API_KEY=your_render_api_key

# List services
render services --output text

# Get service details
render services get your_service_id --output json

# Check deployment status
render deploys list your_service_id --output text

# View logs
render logs -r your_service_id --output text

# Trigger deployment
render deploys create your_service_id --confirm --output text

# Access PostgreSQL database
render psql your_database_id
```

## Troubleshooting

- Check application logs for errors
- Verify environment variables are set correctly
- Ensure Google OAuth credentials are correct
- Check database connection settings
- Verify static files configuration
