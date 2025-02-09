# Turkish Legal AI Assistant

A RAG-based question-answering system for Turkish legal documents.

## Development

Please follow our [Development Workflow](WORKFLOW.md) for all contributions.

## Quick Start

### Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```

### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

## Project Structure
```
.
├── backend/          # FastAPI backend
│   ├── app/         # API endpoints
│   ├── src/         # Core logic
│   └── tests/       # Test files
└── frontend/        # React frontend
```

## API Endpoints

- `POST /api/v1/qa`: Ask legal questions
- `GET /api/v1/health`: Health check

## Contributing

1. Fork the repository
2. Create your feature branch
3. Make your changes
4. Submit a pull request
