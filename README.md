# Turkish Criminal Law QA System

A Retrieval-Augmented Generation (RAG) based question-answering system for the Turkish Criminal Law. This system combines the power of vector embeddings, semantic search, and large language models to provide accurate answers to questions about Turkish Criminal Law.

## Features

- **Web Interface**: Modern React frontend with FastAPI backend
- **Docker Support**: Fully containerized development and production environments
- **Hot Reload**: Automatic code reloading for rapid development
- **Multilingual Support**: Uses a multilingual sentence transformer model for text embeddings
- **Vector-based Search**: Utilizes ChromaDB for efficient similarity search
- **Flexible Querying**: Supports both semantic search and metadata filtering
- **Structured Data Processing**: Handles hierarchical legal text (books, parts, chapters, articles)
- **Error Handling**: Robust error handling and input validation
- **Modular Design**: Separate components for RAG and QA chain
- **Automatic Collection Management**: Handles existing and new ChromaDB collections
- **Configurable LLM Integration**: Works with different language models through LangChain

## Prerequisites

- Docker and Docker Compose
- OpenAI API key (with billing enabled)
- Hugging Face token (optional, but recommended for better performance)
- At least 8GB RAM recommended
- Sufficient disk space for vector storage and Docker images

## Project Structure

```
legal-ai/
├── backend/                 # Backend service
│   ├── app/                # FastAPI application
│   │   ├── api/           # API endpoints
│   │   ├── core/          # Core configuration
│   │   └── services/      # Business logic
│   ├── src/               # RAG system components
│   │   ├── rag/          # RAG implementation
│   │   └── utils/        # Utility functions
│   ├── requirements.txt   # Python dependencies
│   └── Dockerfile        # Backend container definition
├── frontend/              # Frontend service
│   ├── src/              # React application source
│   ├── public/           # Static assets
│   ├── package.json      # Node.js dependencies
│   └── Dockerfile        # Frontend container definition
├── data/                 # Data files
│   ├── raw/              # Raw input files
│   └── processed/        # Processed data files
├── docker-compose.yml    # Production container orchestration
├── docker-compose.dev.yml # Development container orchestration
└── README.md            # Project documentation
```

## Development Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd legal-ai
```

2. Create a `.env` file in the backend directory:
```bash
OPENAI_API_KEY=your_openai_api_key
HUGGINGFACE_TOKEN=your_huggingface_token  # Optional
```

3. Build the Docker images (first time only):
```bash
docker compose build
```

4. Start the development environment:
```bash
docker compose -f docker-compose.dev.yml up
```

The development environment includes:
- Hot reload for both frontend and backend
- Pre-cached models for faster startup
- Development-specific configurations
- Health checks for service coordination

## Development Workflow

1. Frontend Development:
   - Edit files in `frontend/src/`
   - Changes are automatically reflected
   - Access the UI at http://localhost:80

2. Backend Development:
   - Edit files in `backend/`
   - Changes are automatically reloaded
   - Access the API at http://localhost:8000
   - API documentation at http://localhost:8000/api/v1/docs

3. Container Management:
   - View logs: `docker compose -f docker-compose.dev.yml logs -f`
   - Restart services: `docker compose -f docker-compose.dev.yml restart`
   - Stop services: `docker compose -f docker-compose.dev.yml down`

## Production Deployment

For production deployment:

```bash
docker compose up -d
```

## API Documentation

The API documentation is available at `/api/v1/docs` when the backend is running. It provides:
- Interactive API testing
- Request/response schemas
- Authentication details
- Available endpoints

## Error Handling

The system includes comprehensive error handling for:
- Invalid input validation
- File not found errors
- JSON parsing errors
- API errors (OpenAI and Hugging Face)
- Retrieval errors
- Empty or invalid responses
- Collection management errors
- Environment variable configuration errors

## Troubleshooting

Common issues and solutions:
1. OpenAI API errors: Ensure billing is enabled and API key is correct
2. Memory issues: Reduce batch size or number of results
3. Performance issues: Enable Hugging Face token for faster embedding
4. Collection errors: Check disk space and permissions
5. Docker issues: 
   - Ensure Docker Desktop is running
   - Check container logs with `docker compose logs`
   - Verify environment variables in .env file

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

[Your License Here]

## Acknowledgments

- OpenAI for GPT models
- Sentence Transformers for multilingual embeddings
- ChromaDB for vector storage
- LangChain for the chain implementation
- Hugging Face for transformer models
- FastAPI for the backend framework
- React for the frontend framework
