#!/bin/bash

# CreatorPulse Backend Start Script

echo "🚀 Starting CreatorPulse Backend..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "⚠️  Warning: .env file not found!"
    echo "📝 Please create a .env file with your configuration."
    echo "   See .env.example for reference."
    exit 1
fi

# Install/update dependencies
echo "📥 Installing dependencies..."
pip install -q -r requirements.txt

# Start the server
echo "✨ Starting FastAPI server..."
echo "📡 API will be available at http://localhost:8000"
echo "📚 API docs at http://localhost:8000/docs"
echo ""

uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

