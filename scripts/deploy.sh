#!/bin/bash
# Django Template Deployment Script

set -e  # Exit on any error

echo "🚀 Django Template Deployment Script"
echo "===================================="

# Check if we're in the right directory
if [ ! -f "requirements.txt" ]; then
    echo "❌ Error: requirements.txt not found. Run this script from the project root."
    exit 1
fi

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check dependencies
echo "📋 Checking dependencies..."

if ! command_exists python3; then
    echo "❌ Python 3 is required but not installed."
    exit 1
fi

if ! command_exists git; then
    echo "❌ Git is required but not installed."
    exit 1
fi

echo "✅ Dependencies check passed"

# Function for local development setup
setup_local() {
    echo "🏠 Setting up local development environment..."
    
    # Create virtual environment if it doesn't exist
    if [ ! -d "django_template_env" ]; then
        echo "📦 Creating virtual environment..."
        python3 -m venv django_template_env
    fi
    
    # Activate virtual environment
    echo "🔧 Activating virtual environment..."
    source django_template_env/bin/activate
    
    # Install dependencies
    echo "📥 Installing dependencies..."
    pip install --upgrade pip
    pip install -r requirements.txt
    
    # Run migrations
    echo "🗄️ Running database migrations..."
    cd django_app
    python manage.py migrate
    
    echo "✅ Local setup complete!"
    echo "🚀 Start development server with:"
    echo "   source django_template_env/bin/activate"
    echo "   cd django_app && python manage.py runserver"
}

# Function for Render deployment
deploy_render() {
    echo "☁️ Deploying to Render..."
    
    # Check if RENDER_API_KEY is set
    if [ -z "$RENDER_API_KEY" ]; then
        echo "❌ RENDER_API_KEY environment variable not set."
        echo "   Set it with: export RENDER_API_KEY=your_api_key"
        exit 1
    fi
    
    # Check if service ID is provided
    if [ -z "$1" ]; then
        echo "❌ Service ID required. Usage: ./scripts/deploy.sh render <service-id>"
        exit 1
    fi
    
    SERVICE_ID=$1
    
    # Install Render CLI if not present
    if ! command_exists render; then
        echo "📥 Installing Render CLI..."
        curl -s https://raw.githubusercontent.com/render-oss/cli/main/scripts/install.sh | bash
    fi
    
    # Trigger deployment
    echo "🚀 Triggering Render deployment..."
    render deploys create $SERVICE_ID --confirm
    
    echo "✅ Deployment triggered!"
    echo "📊 Check status with: render deploys list $SERVICE_ID"
}

# Function to show help
show_help() {
    echo "Usage: $0 [command] [options]"
    echo ""
    echo "Commands:"
    echo "  local              Set up local development environment"
    echo "  render <service-id> Deploy to Render"
    echo "  help               Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 local"
    echo "  $0 render srv-abc123"
    echo ""
    echo "Environment Variables:"
    echo "  RENDER_API_KEY     Required for Render deployment"
}

# Main script logic
case "${1:-help}" in
    "local")
        setup_local
        ;;
    "render")
        deploy_render $2
        ;;
    "help"|*)
        show_help
        ;;
esac
