#!/bin/bash

# Exit on error
set -e

echo "Setting up development environment..."

# Create and activate Python virtual environment
echo "Creating Python virtual environment..."
python3 -m venv backend/venv

# Activate virtual environment (this won't persist after script ends)
source backend/venv/bin/activate

# Install Python dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Create necessary directories
echo "Creating necessary directories..."
mkdir -p backend/data/criminal_code \
         backend/data/legal_terms \
         backend/data/chroma_db \
         backend/logs

# Download model (this will cache it in the user's home directory)
echo "Downloading sentence transformer model..."
python3 -c "
from sentence_transformers import SentenceTransformer
print('Downloading model...')
model = SentenceTransformer('sentence-transformers/paraphrase-multilingual-mpnet-base-v2', device='cpu')
print('Model downloaded successfully!')
"

echo "
Development environment setup complete!

To start development:

1. Backend:
   cd backend
   source venv/bin/activate  # On Windows use: venv\\Scripts\\activate
   uvicorn main:app --host 0.0.0.0 --port 8000 --reload --log-level debug

2. Frontend:
   cd frontend
   npm install
   npm run dev

Note: Make sure to activate the virtual environment (step 1) whenever you work on the backend.
"