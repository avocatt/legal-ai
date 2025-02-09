# Turkish Legal AI Assistant

A comprehensive AI assistant for Turkish legal research and analysis.

## Implementation Status

- ✅ RAG System
- ✅ Frontend UI
- ✅ Backend API
- ✅ Data Processing

## Overview

Turkish Legal AI Assistant is an advanced question-answering system designed to help users understand Turkish legal concepts and documents. It uses state-of-the-art RAG (Retrieval-Augmented Generation) technology to provide accurate and contextual responses to legal queries in Turkish.

Key features:

- Advanced RAG system for accurate responses
- Comprehensive Turkish legal document processing
- User-friendly interface for legal research
- Integration with major Turkish legal databases

## Quick Start

1. **Clone the Repository**

   ```bash
   git clone https://github.com/yourusername/legal-ai.git
   cd legal-ai
   ```

2. **Run Setup Script**

   ```bash
   ./scripts/setup/setup_dev.sh
   ```

3. **Start Services**

   ```bash
   # Start backend
   cd backend
   poetry run uvicorn app.main:app --reload

   # Start frontend (in another terminal)
   cd frontend
   npm run dev
   ```

4. **Access the Application**
   - Frontend: http://localhost:3000
   - API: http://localhost:8000
   - API Docs: http://localhost:8000/docs

## Project Structure

```
.
├── .github/                    # GitHub and CI/CD
│   ├── workflows/             # GitHub Actions
│   ├── scripts/               # Development automation
│   └── ISSUE_TEMPLATE/        # Issue templates
├── backend/                   # Backend service
│   ├── app/                  # Application entry
│   ├── src/                  # Core business logic
│   ├── tests/                # Test files
│   ├── migrations/           # Database migrations
│   ├── chroma_db/           # Vector store data
│   └── logs/                 # Application logs
├── frontend/                  # Frontend service
│   ├── src/                  # Source code
│   ├── public/               # Static files
│   └── tests/                # Test files
├── data/                      # Project data
│   ├── raw/                  # Raw data files
│   └── processed/            # Processed data
├── docs/                      # Documentation
│   ├── api/                  # API documentation
│   ├── backend/              # Backend documentation
│   └── frontend/             # Frontend documentation
├── config/                    # Configuration files
├── scripts/                   # Development scripts
└── tools/                     # Project tools
```

## Prerequisites

- Python 3.9+
- Node.js 16+
- Docker and Docker Compose
- Git

## Development

Please follow our [Development Workflow](WORKFLOW.md) for all contributions.

## Contributing

We welcome contributions! Please follow these steps:

1. Read our [Contributing Guidelines](CONTRIBUTING.md)
2. Fork the repository
3. Create your feature branch
4. Make your changes
5. Run tests and checks
6. Submit a pull request

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed information.

## Testing

```bash
# Backend tests
cd backend
poetry run pytest

# Frontend tests
cd frontend
npm test
```

## Documentation

- [Readme](docs/README.md)
- [Roadmap](docs/ROADMAP.md)

## License

[Add your license information here]
