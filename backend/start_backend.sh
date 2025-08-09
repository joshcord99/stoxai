#!/bin/bash

# Start the Flask backend with virtual environment
echo "Starting StockAI Backend..."

# Activate virtual environment
source venv/bin/activate

# Install dependencies if needed
echo "Installing dependencies..."
pip install -r requirements.txt

# Start the Flask server
echo "Starting Flask server on port 5003..."
python run_server.py
