#!/bin/bash
# Update requirements using pip-tools

set -e

echo "📦 Updating requirements..."

# Check if pip-tools is installed
if ! pip show pip-tools >/dev/null 2>&1; then
    echo "📥 Installing pip-tools..."
    pip install pip-tools
fi

# Generate requirements.txt from requirements.in
echo "🔄 Generating requirements.txt from requirements.in..."
pip-compile requirements.in

# Install updated requirements
echo "📥 Installing updated requirements..."
pip install -r requirements.txt

echo "✅ Requirements updated successfully!"
echo ""
echo "📋 Summary:"
echo "  - requirements.in: High-level dependencies"
echo "  - requirements.txt: Complete dependencies (auto-generated)"
echo ""
echo "💡 To add a new dependency:"
echo "  1. Add it to requirements.in"
echo "  2. Run: ./scripts/update-requirements.sh"
