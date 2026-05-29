"""Backend API documentation."""
# Backend API Documentation

## Overview
FastAPI backend for Multimodal RAG Chatbot providing REST API endpoints for chat, document processing, and configuration.

## Base URL
- Development: `http://localhost:8000`
- Production: `{base_url}/api`

## Installation

### Install Backend Dependencies
```bash
pip install -r backend/requirements.txt
```

### Run Backend Server
```bash
uvicorn backend.api.main:app --reload --host 0.0.0.0 --port 8000
```

### API Documentation
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Endpoints

### Health Check
**GET** `/api/health`
```bash
curl http://localhost:8000/api/health
```

Response:
```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:30:00.000Z"
}
```

### Chat Endpoints

#### Send Message
**POST** `/api/chat`

Query Parameters:
- `question` (string, required): User question
- `include_summary` (boolean, optional): Include document summary
- `language` (string, optional): Query language

```bash
curl -X POST "http://localhost:8000/api/chat?question=What%20is%20AI?" \
  -H "Content-Type: application/json"
```

Response:
```json
{
  "question": "What is AI?",
  "answer": "Artificial Intelligence...",
  "citations": [...],
  "summary": "...",
  "original_language": "en",
  "retrieved_documents": 3
}
```

#### Get Chat History
**GET** `/api/chat-history`

```bash
curl http://localhost:8000/api/chat-history
```

#### Clear Chat History
**DELETE** `/api/chat-history`

```bash
curl -X DELETE http://localhost:8000/api/chat-history
```

### Document Endpoints

#### Upload Document
**POST** `/api/documents/upload`

```bash
curl -X POST "http://localhost:8000/api/documents/upload" \
  -F "file=@document.pdf"
```

Response:
```json
{
  "status": "success",
  "file_name": "document.pdf",
  "chunks_added": 15,
  "total_documents": 45
}
```

### Language Endpoints

#### Get Supported Languages
**GET** `/api/languages`

```bash
curl http://localhost:8000/api/languages
```

#### Detect Language
**POST** `/api/detect-language`

Query Parameters:
- `text` (string, required): Text to detect

```bash
curl -X POST "http://localhost:8000/api/detect-language?text=Bonjour"
```

### Settings Endpoints

#### Get Settings
**GET** `/api/settings`

```bash
curl http://localhost:8000/api/settings
```

### Statistics

#### Get Stats
**GET** `/api/stats`

```bash
curl http://localhost:8000/api/stats
```

Response:
```json
{
  "total_documents": 45,
  "embedding_dim": 384,
  "chat_history_length": 12,
  "model_name": "sentence-transformers/all-MiniLM-L6-v2"
}
```

#### Get Index Stats
**GET** `/api/index/stats`

### Index Management

#### Save Index
**POST** `/api/index/save`

```bash
curl -X POST http://localhost:8000/api/index/save
```

## Error Handling

All errors return appropriate HTTP status codes:

| Status | Description |
|--------|-------------|
| 200 | Success |
| 400 | Bad Request |
| 500 | Internal Server Error |

Error Response:
```json
{
  "detail": "Error message"
}
```

## CORS

CORS is enabled for all origins in development. Configure in production:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],
    ...
)
```

## Rate Limiting

No rate limiting by default. Add in production:

```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
```

## Authentication

Currently no authentication. Add JWT in production:

```python
from fastapi.security import HTTPBearer
security = HTTPBearer()

@app.post("/api/chat")
async def chat(credentials: HTTPAuthCredentials = Depends(security)):
    ...
```

## Testing

### Run Tests
```bash
pytest tests/
```

### Test API Endpoint
```bash
curl -X GET http://localhost:8000/api/health
```

## Deployment

### Docker
```bash
docker build -f backend/Dockerfile -t rag-backend:latest .
docker run -p 8000:8000 rag-backend:latest
```

### Docker Compose
```bash
docker-compose up -d
```

### Production Server
```bash
gunicorn backend.api.main:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000
```

## Performance

- Response times: < 2s for most queries
- File upload: Up to 100MB (configurable)
- Concurrent connections: Unlimited (configurable)

## See Also
- [Frontend Documentation](../frontend/README.md)
- [Main README](../README.md)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
