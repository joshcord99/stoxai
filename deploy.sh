#!/bin/bash

echo "StoxAI Netlify Deployment Script"
echo "================================="

# Check if Netlify CLI is installed
if ! command -v netlify &> /dev/null; then
    echo "Netlify CLI not found. Installing..."
    npm install -g netlify-cli
fi

# Check if we're in the right directory
if [ ! -f "package.json" ]; then
    echo "Error: package.json not found. Please run this script from the stoxai directory."
    exit 1
fi

# Install dependencies
echo "Installing dependencies..."
npm install

# Build the project
echo "Building the project..."
npm run build

# Check if build was successful
if [ ! -d "dist" ]; then
    echo "Error: Build failed. dist directory not found."
    exit 1
fi

echo "Build successful!"

# Check if netlify.toml exists
if [ ! -f "netlify.toml" ]; then
    echo "Error: netlify.toml not found. Please ensure the Netlify configuration is set up."
    exit 1
fi

echo ""
echo "Next steps:"
echo "1. Push your code to GitHub"
echo "2. Connect your repository to Netlify"
echo "3. Set the following environment variables in Netlify:"
echo "   - JWT_SECRET_KEY=your-jwt-secret-key"
echo "   - NETLIFY_DATABASE_URL=your-neon-database-url"
echo "   - NETLIFY_DATABASE_URL_UNPOOLED=your-neon-database-url-unpooled"
echo "4. Claim your Neon database to prevent expiration"
echo ""
echo "Your application is ready for deployment!"
