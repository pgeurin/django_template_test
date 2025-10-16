#!/bin/bash
set -e

# Get the project ID
PROJECT_ID=$(gcloud config get-value project)
echo "Setting up OAuth credentials for project: $PROJECT_ID"

# Create OAuth consent screen
echo "Creating OAuth consent screen..."
gcloud alpha iap oauth-brands create \
  --application_title="Django Template" \
  --support_email="admin@example.com"

# Create OAuth client ID
echo "Creating OAuth client ID..."
CLIENT_ID_JSON=$(gcloud alpha iap oauth-clients create \
  --display_name="Django Template Web Client" \
  --brand="projects/$PROJECT_ID/brands/1" \
  --oauth_client_type=web \
  --format=json)

# Extract client ID and secret
CLIENT_ID=$(echo $CLIENT_ID_JSON | jq -r '.name' | sed 's/.*\/\([^\/]*\)$/\1/')
CLIENT_SECRET=$(echo $CLIENT_ID_JSON | jq -r '.secret')

echo "OAuth client created successfully!"
echo "Client ID: $CLIENT_ID"
echo "Client Secret: $CLIENT_SECRET"

# Create a file with the credentials
cat > google_oauth_credentials.json << EOL
{
  "web": {
    "client_id": "$CLIENT_ID",
    "project_id": "$PROJECT_ID",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_secret": "$CLIENT_SECRET",
    "redirect_uris": [
      "http://localhost:8000/accounts/google/login/callback/",
      "http://127.0.0.1:8000/accounts/google/login/callback/"
    ],
    "javascript_origins": [
      "http://localhost:8000",
      "http://127.0.0.1:8000"
    ]
  }
}
EOL

echo "Credentials saved to google_oauth_credentials.json"

# Instructions for Django setup
echo ""
echo "To set up in Django admin:"
echo "1. Go to http://127.0.0.1:8000/admin/"
echo "2. Log in with admin@example.com / adminpassword"
echo "3. Go to Social Applications"
echo "4. Add a new Social Application:"
echo "   - Provider: Google"
echo "   - Name: Google"
echo "   - Client ID: $CLIENT_ID"
echo "   - Secret key: $CLIENT_SECRET"
echo "   - Sites: Add your site (usually 'example.com' or your domain)"
echo ""
echo "Then you can use Google login at: http://127.0.0.1:8000/accounts/login/"
