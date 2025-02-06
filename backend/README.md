# Backend Service

## Architecture

The backend service is built with FastAPI and implements a RAG (Retrieval Augmented Generation) system for Turkish legal question answering.

### Core Components

```
backend/
├── app/                    # FastAPI application
│   ├── api/               # API endpoints
│   ├── core/              # Core configurations
│   └── services/          # Business logic
├── src/                   # Core RAG implementation
│   └── rag/              # RAG system components
│       ├── prompts/      # Prompt templates
│       ├── embeddings.py # Embedding utilities
│       ├── rag_system.py # Main RAG implementation
│       └── qa_chain.py   # Question answering chain
└── tests/                # Test suites
```

## Components

### RAG System
- Implements retrieval-augmented generation for legal QA
- Uses ChromaDB for vector storage
- Integrates with OpenAI's GPT models
- Handles both law articles and legal terminology

### Prompt Templates
- Basic legal prompt
- Structured legal prompt
- Multi-step reasoning prompt
- Evaluation metrics and testing framework

### API Layer
- RESTful endpoints for QA
- Request/Response validation
- Error handling middleware
- API documentation (Swagger/OpenAPI)

## Setup

1. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your API keys
```

4. Run the server:
```bash
PYTHONPATH=$PWD uvicorn app.main:app --reload
```

## Development

### Code Style
- Follow PEP 8 guidelines
- Use type hints
- Document functions and classes
- Keep functions focused and small

### Testing
```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_rag_system.py

# Run with coverage
pytest --cov=src tests/
```

### Adding New Features
1. Create feature branch
2. Implement changes
3. Add tests
4. Update documentation
5. Create pull request

## API Documentation

### Main Endpoints

#### POST /api/v1/question
Ask a legal question:
```json
{
  "question": "string",
  "metadata_filter": {
    "book": "string"
  },
  "n_results": 5
}
```

Response:
```json
{
  "answer": "string",
  "confidence_score": 0.8,
  "sources": [
    {
      "id": "string",
      "content": "string",
      "metadata": {},
      "distance": 0.0
    }
  ],
  "processing_time": 0.0
}
```

## Maintenance

### Vector Store
- Regular backups of ChromaDB
- Periodic reindexing
- Performance monitoring

### Model Updates
- Test new model versions
- Update prompt templates
- Validate performance metrics

### Error Handling
- Log monitoring
- Error tracking
- Performance metrics 