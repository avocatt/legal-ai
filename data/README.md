# Data Directory Structure

This directory contains all the data files used by the Turkish Legal AI system. The structure is organized to maintain a clear separation between raw data, processed data, and vector embeddings.

## Directory Structure

```
data/
├── raw/                    # Raw, unprocessed input files
│   ├── criminal_law/      # Raw criminal law documents
│   │   └── türk-ceza-kanunu.pdf  # Turkish Criminal Law PDF
│   └── legal_terms/       # Raw legal terminology data
│       └── legal_terms.json      # Scraped legal terms
│
├── processed/             # Processed and structured data
│   ├── criminal_law/     # Processed criminal law files
│   │   ├── processed_law.json    # Processed law articles
│   │   └── structured_law.json   # Structured law data
│   └── legal_terms/      # Processed legal terminology
│       └── legal_terms.json      # Cleaned and processed terms
│
└── vector_store/         # Vector embeddings and indices
    ├── criminal_law/     # Law article embeddings
    └── legal_terms/      # Legal term embeddings
```

## Data Processing Flow

1. **Raw Data Collection**
   - Criminal law documents are stored in PDF format
   - Legal terms are scraped and stored in JSON format

2. **Data Processing**
   - Raw PDFs are processed into structured JSON
   - Legal terms are cleaned and normalized
   - All processed data maintains references to source material

3. **Vector Storage**
   - Processed data is embedded using sentence transformers
   - Embeddings are stored in ChromaDB format
   - Separate collections for law articles and legal terms

## File Descriptions

### Raw Data
- `türk-ceza-kanunu.pdf`: Original Turkish Criminal Law document
- `legal_terms.json`: Raw scraped legal terminology

### Processed Data
- `processed_law.json`: Extracted and processed law articles
- `structured_law.json`: Hierarchical structure of the law
- `legal_terms.json`: Cleaned and normalized legal terms

### Vector Store
- Contains ChromaDB collections for efficient similarity search
- Separate indices for law articles and legal terminology

## Usage Guidelines

1. Never modify raw data files directly
2. Always maintain backups of processed data
3. Use appropriate scripts in the tools directory for data processing
4. Keep vector store collections in sync with processed data

## Data Update Process

1. Place new raw data in the appropriate raw/ subdirectory
2. Run processing scripts from the tools directory
3. Verify processed output in the processed/ directory
4. Update vector store collections as needed

## Maintenance

- Regular backups of all data directories
- Version control for processed data
- Periodic validation of data integrity
- Documentation of any manual data corrections 