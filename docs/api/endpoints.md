# API Endpoints

## Question Answering

### POST /question

Ask a legal question and get a contextual answer.

#### Request

```json
{
  "question": "string",
  "context_filter": {
    "category": "string",
    "tags": ["string"]
  },
  "options": {
    "max_tokens": 500,
    "temperature": 0.7,
    "n_results": 5
  }
}
```

#### Response

```json
{
  "data": {
    "answer": "string",
    "confidence": 0.95,
    "sources": [
      {
        "id": "string",
        "content": "string",
        "metadata": {
          "category": "string",
          "tags": ["string"]
        },
        "relevance": 0.85
      }
    ],
    "processing_time": 1.5
  },
  "error": null,
  "status": 200
}
```

## Vector Store Management

### POST /vectors/add

Add documents to the vector store.

#### Request

```json
{
  "documents": [
    {
      "content": "string",
      "metadata": {
        "category": "string",
        "tags": ["string"]
      }
    }
  ],
  "options": {
    "chunk_size": 500,
    "chunk_overlap": 50
  }
}
```

### DELETE /vectors/{document_id}

Remove a document from the vector store.

### GET /vectors/search

Search for similar documents.

#### Query Parameters

- `query`: Search query
- `n_results`: Number of results (default: 5)
- `filter`: JSON metadata filter

## System Status

### GET /status

Get system status and statistics.

#### Response

```json
{
  "data": {
    "status": "healthy",
    "vector_store": {
      "total_documents": 1000,
      "last_updated": "2024-02-08T12:00:00Z"
    },
    "api": {
      "version": "1.0.0",
      "uptime": 3600
    }
  },
  "error": null,
  "status": 200
}
```
