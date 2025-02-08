# API Models

## Request Models

### QuestionRequest

```python
class QuestionRequest(BaseModel):
    question: str
    context_filter: Optional[ContextFilter]
    options: Optional[QuestionOptions]

class ContextFilter(BaseModel):
    category: Optional[str]
    tags: Optional[List[str]]

class QuestionOptions(BaseModel):
    max_tokens: Optional[int] = 500
    temperature: Optional[float] = 0.7
    n_results: Optional[int] = 5
```

### VectorAddRequest

```python
class VectorAddRequest(BaseModel):
    documents: List[Document]
    options: Optional[VectorOptions]

class Document(BaseModel):
    content: str
    metadata: Optional[Dict[str, Any]]

class VectorOptions(BaseModel):
    chunk_size: Optional[int] = 500
    chunk_overlap: Optional[int] = 50
```

## Response Models

### QuestionResponse

```python
class QuestionResponse(BaseModel):
    answer: str
    confidence: float
    sources: List[Source]
    processing_time: float

class Source(BaseModel):
    id: str
    content: str
    metadata: Dict[str, Any]
    relevance: float
```

### StatusResponse

```python
class StatusResponse(BaseModel):
    status: str
    vector_store: VectorStoreStatus
    api: ApiStatus

class VectorStoreStatus(BaseModel):
    total_documents: int
    last_updated: datetime

class ApiStatus(BaseModel):
    version: str
    uptime: int
```

### ErrorResponse

```python
class ErrorResponse(BaseModel):
    code: str
    message: str
    details: Optional[Dict[str, Any]]
```

## Common Models

### Metadata

```python
class Metadata(BaseModel):
    category: Optional[str]
    tags: Optional[List[str]]
    source: Optional[str]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
```

### PaginationParams

```python
class PaginationParams(BaseModel):
    page: Optional[int] = 1
    per_page: Optional[int] = 10
    sort_by: Optional[str]
    sort_order: Optional[str] = "asc"
```
