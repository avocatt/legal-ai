# Turkish Legal AI Assistant

> 🚧 **Project Status**: Under Active Development
> 
> Last Updated: February 2025

A modern, AI-powered assistant for Turkish Criminal Law that provides accurate, context-aware answers using RAG (Retrieval Augmented Generation) technology.

## Project Overview

This project implements a comprehensive legal question-answering system specifically designed for Turkish Criminal Law. It combines modern NLP techniques with legal domain knowledge to provide accurate and contextual answers to legal questions.

### Implementation Status

#### Core Features
- [x] Advanced RAG system with ChromaDB vector store
- [x] Legal terminology integration
- [x] Context-aware responses with source citations
- [x] Advanced prompt templates and evaluation
  - Basic legal prompts
  - Structured reasoning prompts
  - Multi-step reasoning prompts
- [x] Comprehensive prompt testing framework
  - Automated evaluation pipeline
  - Multiple evaluation metrics
  - Performance analysis
- [ ] Confidence scoring system (Planned)

#### Frontend
- [x] Modern React frontend with Material-UI
- [x] Basic question-answer interface
- [x] Loading states and error handling
- [x] Markdown rendering support
- [ ] Advanced UI features (In Progress)
- [ ] User session management (Planned)
- [ ] Response history (Planned)

#### Backend
- [x] FastAPI backend with basic endpoints
- [x] Docker containerization
- [x] Basic error handling
- [x] ChromaDB integration
- [x] Prompt template system
- [ ] Advanced error recovery (In Progress)
- [ ] Rate limiting (Planned)
- [ ] Caching layer (Planned)

#### Data Processing
- [x] Basic legal terms processing
- [x] Criminal law article processing
- [x] Vector store management
- [ ] Advanced text preprocessing (In Progress)
- [ ] Multi-source data integration (Planned)
- [ ] Automated updates pipeline (Planned)

## Documentation

Our documentation follows a standardized structure:

- [Documentation Standards](docs/DOCUMENTATION_STANDARDS.md) - Guidelines for maintaining documentation
- [Backend Documentation](backend/README.md) - Backend service architecture and API details
- [Frontend Documentation](frontend/README.md) - Frontend application structure and development
- [Data Documentation](data/README.md) - Data organization and processing pipelines
- [Tools Documentation](tools/README.md) - Development and maintenance tools
- [Technical Documentation](docs/) - Architecture, guides, and technical details
- [Changelog](CHANGELOG.md) - Version history and changes
- [Prompt Documentation](docs/prompts/) - Prompt templates and testing framework

## Quick Start

### Prerequisites
- Python 3.9+
- Node.js 18+
- Docker and Docker Compose (optional)
- OpenAI API key
- Hugging Face token (for embeddings)

### Development Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/legal-ai.git
cd legal-ai
```

2. Set up backend:
```bash
cd backend
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows
pip install -r requirements.txt
```

3. Set up frontend:
```bash
cd frontend
npm install
```

4. Set up environment variables:
```bash
cp backend/.env.example backend/.env
# Edit .env with your API keys
```

### Running with Docker

```bash
docker-compose up --build
```

Access the application:
- Frontend: http://localhost:80
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/api/v1/docs

## Architecture Overview

The system consists of several key components:

1. **RAG System**
   - ChromaDB vector store
   - Multilingual embeddings
   - Context-aware retrieval
   - Legal term integration

2. **Backend Service**
   - FastAPI application
   - RESTful API endpoints
   - Error handling middleware
   - Docker containerization

3. **Frontend Application**
   - React with TypeScript
   - Material-UI components
   - Real-time API integration
   - Responsive design

4. **Data Pipeline**
   - Raw data processing
   - Vector store management
   - Legal term extraction
   - Automated updates

## Known Issues & Limitations

- Currently supports only Turkish Criminal Law
- Limited to GPT-3.5-turbo model
- No user authentication system yet
- Basic error handling implementation
- Rate limiting not implemented
- Limited to single language (Turkish)

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

### Active Development Areas
- Prompt engineering improvements
- Evaluation metrics enhancement
- Error handling refinement
- UI/UX improvements
- Documentation updates
- Test coverage expansion

### Code Style
- Python: PEP 8
- TypeScript: ESLint + Prettier
- Pre-commit hooks for code quality
- Documentation: Markdown

### Testing
- Unit tests required
- Integration tests for critical paths
- End-to-end testing for main flows
- Documentation tests

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Turkish Ministry of Justice for legal resources
- OpenAI for GPT models
- ChromaDB for vector store implementation
- FastAPI and React communities
- Contributors and maintainers

## Support

For support:
1. Check the documentation
2. Open an issue
3. Contact maintainers
4. Join our community discussions
