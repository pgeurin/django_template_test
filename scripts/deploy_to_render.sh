#!/usr/bin/env bash
# Script to deploy to Render using the Render CLI

# Exit on error
set -e

# Check if RENDER_API_KEY is set
if [ -z "$RENDER_API_KEY" ]; then
    echo "Error: RENDER_API_KEY environment variable is not set."
    echo "Please set it using: export RENDER_API_KEY=your_api_key"
    exit 1
fi

# Check if service ID is provided as argument
SERVICE_ID=${1:-""}
if [ -z "$SERVICE_ID" ]; then
    echo "Error: No service ID provided."
    echo "Usage: ./deploy_to_render.sh <service_id>"
    echo "You can find your service ID in the Render dashboard URL: https://dashboard.render.com/web/srv-XXXXXXXX"
    exit 1
fi

# Set the API key for the Render CLI
export RENDER_API_KEY

echo "Deploying to Render service: $SERVICE_ID"

# Trigger a manual deploy
render deploys create "$SERVICE_ID" --output text

# Check the status of the deployment
echo "Checking deployment status..."
render services get "$SERVICE_ID" --output text

echo "Deployment initiated. You can check the status in the Render dashboard."
echo "Dashboard URL: https://dashboard.render.com/web/$SERVICE_ID"
