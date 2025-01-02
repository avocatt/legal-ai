# Legal-AI: Turkish Criminal Law Question-Answering System

## Table of Contents
1. [Project Overview](#project-overview)
2. [Current Implementation](#current-implementation)
3. [System Architecture](#system-architecture)
4. [Future Goals](#future-goals)
5. [Technologies Used](#technologies-used)
6. [Setup and Usage](#setup-and-usage)
7. [Contributing](#contributing)

## Project Overview
Legal-AI is a Retrieval-Augmented Generation (RAG)-based question-answering system for Turkish Criminal Law. The system helps legal professionals and students retrieve accurate, context-aware information from the Turkish Criminal Code (TCK).

## Current Implementation
- **Text Extraction**: Implemented PDF text extraction using `pdfplumber` with support for Turkish characters
- **Text Processing**: 
  - Structured law text into hierarchical format (books, parts, chapters, articles)
  - Cleaned OCR artifacts and formatting issues
  - Extracted key provisions from articles
- **RAG System**:
  - Implemented semantic search using multilingual sentence transformers
  - Built vector storage using ChromaDB
  - Integrated GPT-4 for context-aware answer generation

## System Architecture
The system consists of several components:
1. **PDF Processing** (`pdf_extractor.py`):
   - Extracts text from PDF using pdfplumber
   - Compares extraction quality between different libraries

2. **Law Text Processing** (`law_processor.py`, `text_processor.py`):
   - Structures the law into hierarchical JSON format
   - Cleans text and extracts key provisions
   - Handles Turkish language specifics

3. **QA System** (`rag_system.py`):
   - Uses sentence-transformers for semantic embeddings
   - Stores and retrieves relevant context using ChromaDB
   - Generates accurate answers using GPT-4

## Future Goals
- [ ] Implement a web-based user interface
- [ ] Add support for multiple legal documents
- [ ] Improve answer generation with legal-specific fine-tuning
- [ ] Add citation verification and validation
- [ ] Implement user feedback collection and system improvement
- [ ] Add support for complex legal queries and case analysis

## Technologies Used
- **Core Technologies**:
  - Python 3.11+
  - LangChain for RAG implementation
  - ChromaDB for vector storage
  - Sentence-Transformers for embeddings
  - OpenAI GPT-4 for answer generation
- **Text Processing**:
  - pdfplumber for PDF extraction
  - regex for text cleaning
- **Dependencies**:
  - sentence-transformers
  - chromadb
  - langchain
  - pdfplumber
  - openai
  - python-dotenv

## Setup and Usage
1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Set up your OpenAI API key in `.env`
4. Process the law text:
   ```bash
   python pdf_extractor.py
   python law_processor.py
   python text_processor.py
   ```
5. Run the QA system:
   ```bash
   python rag_system.py
   ```

## Contributing
Contributions are welcome! Please feel free to submit issues and pull requests.
