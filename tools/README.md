# Project Tools

This directory contains various tools and utilities for the Legal AI project.

## Directory Structure

```
tools/
├── data_processing/          # Data processing utilities
│   ├── vector_store/        # Vector store management
│   ├── terminology/         # Legal terminology processing
│   ├── analyze_criminal_law_content.py
│   ├── filter_criminal_law_articles.py
│   ├── clean_criminal_law_articles.py
│   └── README.md
├── analysis/                # Analysis tools
├── deployment/              # Deployment utilities
├── scripts/                 # Utility scripts
└── hierarchy/               # Hierarchy management
```

## Tools Overview

### Data Processing

The `data_processing` directory contains tools for processing legal documents and managing the vector store:

- `vector_store/`: Tools for managing and maintaining the vector database
- `terminology/`: Tools for processing and managing legal terminology
- `analyze_criminal_law_content.py`: Analyzes criminal law content
- `filter_criminal_law_articles.py`: Filters relevant criminal law articles
- `clean_criminal_law_articles.py`: Cleans and preprocesses criminal law articles

### Analysis Tools

The `analysis` directory contains tools for analyzing the system's performance and data quality.

### Deployment Tools

The `deployment` directory contains utilities for deploying the application in various environments.

### Scripts

The `scripts` directory contains various utility scripts for development and maintenance.

### Hierarchy

The `hierarchy` directory contains tools for managing the legal document hierarchy.

## Usage

Each tool directory contains its own README with specific usage instructions.

## Contributing

When adding new tools:

1. Follow the established directory structure
2. Use consistent naming (use underscores for Python-related directories)
3. Include proper documentation
4. Add tests where appropriate
