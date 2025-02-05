# Turkish Legal AI Assistant

A modern, AI-powered assistant for Turkish Criminal Law that provides accurate, context-aware answers using RAG (Retrieval Augmented Generation) technology.

## Features

### Core Functionality
- Advanced RAG system with ChromaDB vector store
- Legal terminology integration and context-aware responses
- Intelligent question-answering with source citations
- Metadata-based filtering for specific law sections
- Smart handling of out-of-scope questions and insufficient context

### Technical Features
- FastAPI backend with modern LangChain integration
- React frontend with TypeScript and Material-UI
- Docker containerization for easy deployment
- Persistent vector storage with ChromaDB
- Comprehensive error handling and response validation

## Getting Started

### Prerequisites
- Python 3.9+
- Node.js 18+
- Docker and Docker Compose (optional)

### Environment Setup
1. Clone the repository:
```bash
git clone https://github.com/yourusername/legal-ai.git
cd legal-ai
```

2. Set up environment variables:
```bash
cp backend/.env.example backend/.env
# Edit .env with your OpenAI and Hugging Face API keys
```

### Local Development

#### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows
pip install -r requirements.txt
PYTHONPATH=$PWD uvicorn app.main:app --reload
```

#### Frontend
```bash
cd frontend
npm install
npm run dev
```

### Docker Deployment
```bash
docker-compose up --build
```

## Architecture

### Backend Components
- **RAG System**: Combines retrieval-based and generative approaches
- **Vector Store**: ChromaDB for efficient similarity search
- **Legal Terms**: Specialized handling of legal terminology
- **QA Chain**: Advanced prompt engineering and context management

### Frontend Features
- Modern React with TypeScript
- Material-UI components
- Real-time API integration
- Error handling and loading states

## API Documentation

### Main Endpoints
- `POST /api/v1/question`: Submit a legal question
  ```json
  {
    "question": "string",
    "metadata_filter": {"book": "string"} (optional),
    "n_results": integer (optional)
  }
  ```

## Development Guidelines

### Code Style
- Python: PEP 8
- TypeScript: ESLint + Prettier
- Pre-commit hooks for code quality

### Testing
- Unit tests for core functionality
- Integration tests for API endpoints
- End-to-end testing for critical flows

## Contributing
1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License
This project is licensed under the MIT License - see the LICENSE file for details.
