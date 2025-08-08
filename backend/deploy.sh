#!/bin/bash

# Stock Analyst Backend Deployment Script

set -e

echo "🚀 Starting Stock Analyst Backend deployment..."

# Check if .env file exists
if [ ! -f .env ]; then
    echo "⚠️  .env file not found. Creating from template..."
    cp env.example .env
    echo "📝 Please edit .env file with your configuration before continuing."
    exit 1
fi

# Install dependencies
echo "📦 Installing Python dependencies..."
npm run setup

# Run tests
echo "🧪 Running tests..."
npm run test

# Format code
echo "🎨 Formatting code..."
npm run format

# Lint code
echo "🔍 Linting code..."
npm run lint

# Check health
echo "🏥 Checking service health..."
npm run health
npm run chatbot-health

echo "✅ Deployment completed successfully!"
echo "🌐 Backend API running on: http://localhost:5003"
echo "🤖 Chatbot API running on: http://localhost:5002"
echo ""
echo "📚 Available commands:"
echo "  npm run dev     - Start development server"
echo "  npm start       - Start production server"
echo "  npm run health  - Check API health"
echo "  make help       - Show all available commands" 