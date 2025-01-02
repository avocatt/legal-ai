# Turkish Criminal Law QA System

A Retrieval-Augmented Generation (RAG) based question-answering system for the Turkish Criminal Law. This system combines the power of vector embeddings, semantic search, and large language models to provide accurate answers to questions about Turkish Criminal Law.

## Features

- **Multilingual Support**: Uses a multilingual sentence transformer model for text embeddings
- **Vector-based Search**: Utilizes ChromaDB for efficient similarity search
- **Flexible Querying**: Supports both semantic search and metadata filtering
- **Structured Data Processing**: Handles hierarchical legal text (books, parts, chapters, articles)
- **Error Handling**: Robust error handling and input validation
- **Modular Design**: Separate components for RAG and QA chain
- **Automatic Collection Management**: Handles existing and new ChromaDB collections
- **Configurable LLM Integration**: Works with different language models through LangChain

## Prerequisites

- Python 3.8+
- OpenAI API key (with billing enabled)
- Hugging Face token (optional, but recommended for better performance)
- At least 8GB RAM recommended
- Sufficient disk space for vector storage

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd legal-ai
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the project root:
```bash
OPENAI_API_KEY=your_openai_api_key
HUGGINGFACE_TOKEN=your_huggingface_token  # Optional
```

## Project Structure

```
legal-ai/
├── src/                      # Source code
│   ├── rag/                  # RAG system components
│   │   ├── __init__.py      # Package exports
│   │   ├── embeddings.py    # Embedding functionality
│   │   ├── retriever.py     # Document retrieval logic
│   │   └── qa_chain.py      # QA chain implementation
│   ├── processors/          # Data processing
│   │   └── __init__.py      # Package exports
│   └── utils/               # Utility functions
│       ├── __init__.py      # Package exports
│       └── helpers.py       # Helper functions
├── data/                    # Data files
│   ├── raw/                 # Raw input files
│   │   └── türk-ceza-kanunu.pdf
│   ├── processed/          # Processed data files
│   │   └── processed_law.json
│   └── vector_store/       # Vector database files
├── tests/                  # Test files
│   ├── __init__.py        # Test package marker
│   └── test_rag.py        # RAG system tests
├── examples/              # Example scripts
│   └── basic_usage.py    # Basic usage example
├── notebooks/            # Jupyter notebooks
│   └── system_demo.ipynb # Interactive system demo
├── .env                  # Environment variables
├── .gitignore           # Git ignore patterns
├── requirements.txt      # Project dependencies
├── setup.py             # Package setup configuration
├── pytest.ini           # Pytest configuration
├── .flake8             # Flake8 configuration
├── README.md           # Project documentation
└── LICENSE             # License file
```

## Development Tools

The project uses several development tools for quality assurance:

- **pytest**: For unit testing and code coverage
  ```bash
  pytest                # Run all tests
  pytest --cov=src     # Run tests with coverage report
  ```

- **flake8**: For code style and quality checks
  ```bash
  flake8 src tests     # Check code style
  ```

## Usage

### Basic Usage

```python
from legal_ai.rag import TurkishLegalRAG, LegalQAChain
from langchain_openai import ChatOpenAI

# Initialize the RAG system
rag_system = TurkishLegalRAG("data/processed/processed_law.json")

# Initialize LLM
llm = ChatOpenAI(
    model_name="gpt-3.5-turbo",
    temperature=0
)

# Create QA chain
qa_chain = LegalQAChain(rag_system, llm)

# Ask a question
question = "Ceza kanununun temel amacı nedir?"
answer = qa_chain.run(question)
print(answer)
```

### Interactive Demo

The project includes a Jupyter notebook (`notebooks/system_demo.ipynb`) that demonstrates:
- Basic question answering
- Metadata filtering
- Custom prompt templates
- Document retrieval exploration
- Error handling examples

To run the notebook:
```bash
jupyter notebook notebooks/system_demo.ipynb
```

### Metadata Filtering

```python
# Filter questions about specific books
filtered_answer = qa_chain.run(
    "Cezaların türleri nelerdir?",
    metadata_filter={"book": "İKİNCİ KİTAP"}
)
```

### Custom Prompt Templates

```python
from langchain_core.prompts import ChatPromptTemplate

# Create custom prompt
custom_prompt = ChatPromptTemplate.from_messages([
    ("system", "Your custom system message here"),
    ("human", "Context:\n{context}\n\nQuestion: {question}")
])

# Set custom prompt
qa_chain.set_custom_prompt(custom_prompt)
```

## Components

### RAG Module (`src/rag/`)
- `embeddings.py`: Handles text embedding using sentence transformers
- `retriever.py`: Manages document retrieval and vector store operations
- `qa_chain.py`: Implements the question-answering chain

### Utils Module (`src/utils/`)
- `helpers.py`: Provides utility functions for file operations and API key validation

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
