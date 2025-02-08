#!/bin/bash

# Exit on error
set -e

echo "🚀 Setting up development environment..."

# Check for required tools
echo "📋 Checking prerequisites..."
command -v python3 >/dev/null 2>&1 || { echo "❌ Python 3 is required but not installed."; exit 1; }
command -v node >/dev/null 2>&1 || { echo "❌ Node.js is required but not installed."; exit 1; }
command -v poetry >/dev/null 2>&1 || { echo "⚙️ Installing Poetry..."; curl -sSL https://install.python-poetry.org | python3 -; }

# Setup Python environment
echo "🐍 Setting up Python environment..."
cd backend
poetry install
poetry run pre-commit install

# Setup frontend
echo "🌐 Setting up frontend..."
cd ../frontend
npm install

# Setup git hooks
echo "🔧 Setting up git hooks..."
cd ..
pre-commit install

# Copy environment files
echo "⚙️ Setting up environment files..."
cp config/development/.env.example config/development/.env
cp config/development/.env.example backend/.env

# Create necessary directories
echo "📁 Creating necessary directories..."
mkdir -p data/raw
mkdir -p data/processed

echo "✅ Development environment setup complete!"
echo "
Next steps:
1. Update config/development/.env with your settings
2. Start the development servers:
   - Backend: cd backend && poetry run uvicorn app.main:app --reload
   - Frontend: cd frontend && npm run dev
"
