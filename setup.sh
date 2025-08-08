#!/bin/bash

# Stock Analyst Frontend Setup Script

set -e

echo "🚀 Setting up Stock Analyst Frontend..."

# Check if .env file exists
if [ ! -f .env ]; then
    echo "📝 Creating .env file from template..."
    cp env.example .env
    echo "✅ .env file created!"
    echo ""
    echo "📋 Please edit .env file with your backend URL:"
    echo "   - For local development: VITE_BACKEND_URL=http://localhost:5003"
    echo "   - For production: VITE_BACKEND_URL=https://your-backend-api.com"
    echo ""
else
    echo "✅ .env file already exists"
fi

# Install dependencies
echo "📦 Installing dependencies..."
npm install

# Check if backend URL is configured
if grep -q "VITE_BACKEND_URL" .env; then
    BACKEND_URL=$(grep "VITE_BACKEND_URL" .env | cut -d '=' -f2)
    echo "🔗 Backend URL configured: $BACKEND_URL"
else
    echo "⚠️  VITE_BACKEND_URL not found in .env file"
    echo "   Please add: VITE_BACKEND_URL=http://localhost:5003"
fi

echo ""
echo "✅ Frontend setup completed!"
echo ""
echo "📚 Available commands:"
echo "  npm run dev     - Start development server"
echo "  npm run build   - Build for production"
echo "  npm run lint    - Lint code"
echo "  npm run test    - Run tests"
echo ""
echo "🌐 Start development: npm run dev"
echo "🔗 Frontend will be available at: http://localhost:5173" 