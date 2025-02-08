# Backend

## Overview

The backend is built with FastAPI and provides the core functionality for the Legal AI Assistant. It includes the RAG system, API endpoints, and integration with various services like ChromaDB for vector storage.

## Usage

### Development Setup

1. Create and activate a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: .\venv\Scripts\activate
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Start the development server:

   ```bash
   uvicorn app.main:app --reload
   ```

4. Visit [http://localhost:8000/docs](http://localhost:8000/docs) for API documentation.

## Configuration

### Environment Variables

Create a `.env` file in the backend directory:

```env
# API Configuration
API_VERSION=v1
API_PREFIX=/api/v1
DEBUG=True

# OpenAI Configuration
OPENAI_API_KEY=your-api-key
OPENAI_MODEL=gpt-3.5-turbo

# Vector Store Configuration
VECTOR_STORE_PATH=data/vector_store
EMBEDDINGS_MODEL=sentence-transformers/all-mpnet-base-v2

# Security
SECRET_KEY=your-secret-key
CORS_ORIGINS=http://localhost:3000
```

### Project Structure

```
backend/
├── app/
│   ├── api/          # API endpoints
│   ├── core/         # Core functionality
│   ├── models/       # Data models
│   ├── services/     # Business logic
│   └── utils/        # Utility functions
├── data/            # Data storage
├── tests/           # Test files
└── scripts/         # Utility scripts
```

### Key Components

1. **RAG System**

   - ChromaDB integration for vector storage
   - Advanced retrieval strategies
   - Context-aware response generation

2. **API Endpoints**

   - RESTful API design
   - OpenAPI documentation
   - Request validation
   - Error handling

3. **Data Processing**
   - Text preprocessing
   - Vector embeddings
   - Document chunking

### Dependencies

- Python 3.11+
- FastAPI
- ChromaDB
- OpenAI
- SQLAlchemy
- Pydantic
- Alembic
