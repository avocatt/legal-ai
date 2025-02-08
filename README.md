# Legal AI Assistant

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/release/python-3110/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## Implementation Status

- ✅ RAG System
- ✅ Frontend UI
- ✅ Backend API
- ✅ Data Processing

## Documentation

- [Contributing](docs/CONTRIBUTING.md)
- [Documentation Standards](docs/DOCUMENTATION_STANDARDS.md)
- [Git Workflow](docs/GIT_WORKFLOW.md)
- [Readme](docs/README.md)
- [Roadmap](docs/ROADMAP.md)

## Overview

Legal AI Assistant is an advanced question-answering system designed to help users understand legal concepts and documents. It uses state-of-the-art RAG (Retrieval-Augmented Generation) technology to provide accurate and contextual responses to legal queries.

## Quick Start

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/legal-ai.git
   cd legal-ai
   ```

2. Install dependencies:

   ```bash
   # Backend
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: .\venv\Scripts\activate
   pip install -r requirements.txt

   # Frontend
   cd ../frontend
   npm install
   ```

3. Set up environment variables:

   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

4. Run the application:

   ```bash
   # Backend
   cd backend
   uvicorn app.main:app --reload

   # Frontend (in a new terminal)
   cd frontend
   npm run dev
   ```

## Development

### Project Structure

```
legal-ai/
├── backend/           # FastAPI backend
├── frontend/         # React frontend
├── tools/            # Development tools
│   ├── data_processing/  # Data processing scripts
│   ├── vector_store/     # Vector store management
│   └── hierarchy/        # Legal hierarchy tools
└── docs/             # Documentation
```

### Development Workflow

1. Create a new branch for your feature:

   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Make your changes and commit them:

   ```bash
   git add .
   git commit -m "feat: add your feature"
   ```

3. Push your changes and create a pull request:
   ```bash
   git push origin feature/your-feature-name
   ```

### Code Style

We use the following tools to maintain code quality:

- Black for Python code formatting
- ESLint and Prettier for JavaScript/TypeScript
- Pre-commit hooks for automated checks

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes following our commit message conventions
4. Push to your fork
5. Create a Pull Request

Please read [CONTRIBUTING.md](docs/CONTRIBUTING.md) for details on our code of conduct and development process.

## Documentation

See the [docs](docs/) directory for detailed documentation on:

- Architecture Overview
- API Documentation
- Development Guidelines
- Deployment Guide
