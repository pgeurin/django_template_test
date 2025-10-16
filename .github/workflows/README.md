# GitHub Actions Workflows

This directory contains GitHub Actions workflows for automating the deployment process.

## Render Deployment Workflow

The `render-deploy.yml` workflow automatically deploys the application to Render when changes are pushed to the main branch.

### Workflow Steps:

1. **Test**: Runs the Django test suite to ensure all tests pass before deployment
2. **Deploy**: Triggers a deployment to Render using the Render API
3. **Verify**: Waits for the deployment to complete and verifies its success
4. **Notify**: Sends notifications about the deployment status

### Required Secrets:

To use this workflow, you need to set up the following secrets in your GitHub repository:

- `RENDER_SERVICE_ID`: Your Render service ID
- `RENDER_API_KEY`: Your Render API key

### How to Get Render API Key and Service ID:

1. **API Key**:
   - Log in to your Render dashboard
   - Go to Account Settings → API Keys
   - Create a new API key

2. **Service ID**:
   - Go to your web service in the Render dashboard
   - The service ID is in the URL: `https://dashboard.render.com/web/srv-XXXXXXXX`
   - The ID is the `srv-XXXXXXXX` part

### Manual Deployment:

You can also manually trigger the workflow from the GitHub Actions tab by selecting "Run workflow".

## Docker Deployment Workflow

The `docker-deploy.yml` workflow builds and pushes a Docker image to Docker Hub, which can then be deployed to Railway or another container platform.

### Required Secrets:

- `DOCKER_USERNAME`: Your Docker Hub username
- `DOCKER_PASSWORD`: Your Docker Hub password or access token
