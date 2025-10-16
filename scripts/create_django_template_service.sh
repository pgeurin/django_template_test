#!/usr/bin/env bash
# Script to create a new django-template service on Render

# Exit on error
set -e

echo "=== Creating Django Template Service on Render ==="
echo ""
echo "This script will guide you through creating a new service for django_template on Render."
echo ""
echo "Steps:"
echo "1. Make sure your code is pushed to GitHub"
echo "2. Open the Render dashboard in your browser"
echo "3. Create a new Blueprint"
echo ""

# Check if the code is pushed to GitHub
echo "Checking if your code is pushed to GitHub..."
git status

# Open the Render dashboard
echo ""
echo "Please follow these steps:"
echo ""
echo "1. Open the Render dashboard: https://dashboard.render.com/"
echo ""
echo "2. Click on 'New' and select 'Blueprint'"
echo ""
echo "3. Connect to your GitHub repository: pgeurin/django_template"
echo ""
echo "4. Render will automatically detect the render.yaml file and create:"
echo "   - Web service: django-template"
echo "   - PostgreSQL database: django-template-db"
echo ""
echo "5. Click 'Apply' to create the services"
echo ""
echo "6. Wait for the deployment to complete"
echo ""
echo "7. Your application will be available at: https://django-template.onrender.com"
echo ""

# Ask if they want to open the Render dashboard
read -p "Would you like to open the Render dashboard in your browser? (y/n): " open_browser

if [[ $open_browser == "y" || $open_browser == "Y" ]]; then
    echo "Opening Render dashboard..."
    open "https://dashboard.render.com/"
fi

echo ""
echo "After deployment, you can use the Render CLI to manage your service:"
echo ""
echo "# Set your API key"
echo "export RENDER_API_KEY=rnd_jFkvX0CjyciuFPyt2N9nqlqza9Cq"
echo ""
echo "# List your services"
echo "render services --output text"
echo ""
echo "# Create a new deployment"
echo "render deploys create YOUR_SERVICE_ID --confirm --output text"
echo ""
echo "# View logs"
echo "render logs -r YOUR_SERVICE_ID --output text"
echo ""
echo "=== Done ==="
