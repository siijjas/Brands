#!/bin/bash

# Tailor Management App Installation Script
# This script helps with the installation of the app in an ERPNext environment

echo "🧵 Tailor Management App Installation"
echo "====================================="

# Check if we're in a bench directory
if [ ! -d "apps" ] || [ ! -d "sites" ]; then
    echo "❌ Error: This script must be run from the root of a Frappe bench directory"
    echo "Please navigate to your bench directory and run this script again"
    exit 1
fi

# Check if the app already exists
if [ -d "apps/tailor_management" ]; then
    echo "⚠️  Warning: tailor_management app already exists in apps/"
    echo "Please remove it first with: bench remove-app tailor_management"
    exit 1
fi

# Get the app from repository
echo "📦 Getting Tailor Management app from repository..."
bench get-app https://github.com/siijjas/Brands

# Check if installation was successful
if [ ! -d "apps/tailor_management" ]; then
    echo "❌ Failed to download the app"
    exit 1
fi

echo "✅ App downloaded successfully"

# Ask for site name
echo ""
read -p "🌐 Enter your ERPNext site name (e.g., mysite.local): " SITE_NAME

if [ -z "$SITE_NAME" ]; then
    echo "❌ Site name is required"
    exit 1
fi

# Check if site exists
if [ ! -d "sites/$SITE_NAME" ]; then
    echo "❌ Site '$SITE_NAME' does not exist"
    echo "Available sites:"
    ls -1 sites/ | grep -v assets | grep -v common_site_config.json
    exit 1
fi

# Install the app
echo "🔧 Installing Tailor Management app on site '$SITE_NAME'..."
bench --site $SITE_NAME install-app tailor_management

if [ $? -ne 0 ]; then
    echo "❌ Failed to install app on site"
    exit 1
fi

# Run migrations
echo "🔄 Running database migrations..."
bench --site $SITE_NAME migrate

# Build assets
echo "🏗️  Building assets..."
bench build --app tailor_management

# Restart bench (optional)
echo ""
read -p "🔄 Restart bench processes? (y/n): " RESTART_BENCH

if [ "$RESTART_BENCH" = "y" ] || [ "$RESTART_BENCH" = "Y" ]; then
    echo "🔄 Restarting bench..."
    bench restart
fi

echo ""
echo "🎉 Tailor Management App Installation Complete!"
echo ""
echo "📖 Next Steps:"
echo "1. Open your ERPNext site: http://$SITE_NAME"
echo "2. Navigate to the 'Tailor Management' module"
echo "3. Start by creating a Measurement Profile for a customer"
echo "4. Create your first Tailoring Job"
echo "5. Use the Kanban board to manage production workflow"
echo ""
echo "📚 Documentation: See README.md for detailed usage instructions"
echo "🐛 Issues: https://github.com/siijjas/Brands/issues"
echo ""
echo "Happy Tailoring! 🧵✂️👔"