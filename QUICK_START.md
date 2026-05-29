"""Quick Start Guide for the Full Stack Application."""
# Quick Start Guide

## Overview
This is a complete Multimodal RAG Chatbot with:
- **Frontend**: React + TypeScript
- **Backend**: FastAPI + Python
- **Deployment**: Docker & Docker Compose

## Prerequisites
- Docker & Docker Compose (for containerized deployment)
- OR Node.js 18+ and Python 3.10+ (for local development)

## Quick Start Options

### Option 1: Docker Compose (Recommended)

```bash
# 1. Navigate to project directory
cd "c:\Users\ankus\Documents\multi model rag chatbot"

# 2. Build and start all services
docker-compose up -d

# 3. Access the application
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000
# Nginx (combined): http://localhost
```

### Option 2: Local Development

#### Backend Setup
```bash
# 1. Install backend dependencies
pip install -r requirements.txt
pip install -r backend/requirements.txt

# 2. Run FastAPI server
uvicorn backend.api.main:app --reload --host 0.0.0.0 --port 8000

# Server running at: http://localhost:8000
# API docs: http://localhost:8000/docs
```

#### Frontend Setup
```bash
# 1. Navigate to frontend directory
cd frontend

# 2. Install dependencies
npm install

# 3. Configure environment
# Copy .env.example to .env (already configured for localhost)

# 4. Start development server
npm start

# App running at: http://localhost:3000
```

## What's Included

### Frontend (React + TypeScript)
```
frontend/
├── src/
│   ├── components/      # Reusable components
│   ├── hooks/          # Custom React hooks
│   ├── types/          # TypeScript types
│   ├── utils/          # Utility functions & API client
│   ├── styles/         # CSS stylesheets
│   └── index.tsx       # Entry point
├── public/             # Static assets
├── package.json        # Dependencies
├── tsconfig.json       # TypeScript config
└── Dockerfile          # Container image
```

### Backend (FastAPI)
```
backend/
├── api/
│   ├── main.py        # FastAPI application
│   ├── schemas.py     # Pydantic models
│   └── __init__.py
├── requirements.txt   # Python dependencies
├── Dockerfile        # Container image
└── README.md        # API documentation
```

### Core Application
```
src/
├── rag_chatbot.py              # Main chatbot class
├── document_processor.py       # PDF/Image processing
├── embeddings.py              # FAISS embeddings
├── retriever.py               # Semantic search
├── summarizer.py              # Document summarization
├── citation_extractor.py      # Citation extraction
├── multilingual.py            # Language support
└── llm_interface.py          # LLM generation
```

## Features

### Chat Interface
- Real-time message display with animations
- Auto-scroll to latest message
- Loading indicators
- Error handling

### Document Upload
- Drag & drop interface
- Multiple file support
- Progress tracking
- Supported formats: PDF, TXT, JPG, PNG, GIF

### Citations & References
- Expandable citations viewer
- Direct links to sources
- Citation formatting (APA, MLA, Chicago)
- Author and year information

### Settings
- Model configuration display
- Supported languages list
- Index statistics
- Real-time updates

### Sidebar Navigation
- Document counter
- Chat history tracking
- Dark/Light theme toggle
- Quick action buttons
- Live statistics

## API Endpoints

### Health
- `GET /api/health` - Check API status

### Chat
- `POST /api/chat` - Send message
- `GET /api/chat-history` - Get conversation history
- `DELETE /api/chat-history` - Clear history

### Documents
- `POST /api/documents/upload` - Upload document

### Languages
- `GET /api/languages` - Get supported languages
- `POST /api/detect-language` - Detect language

### Settings
- `GET /api/settings` - Get configuration

### Index
- `POST /api/index/save` - Save FAISS index
- `GET /api/index/stats` - Index statistics

## Configuration

### Environment Variables

#### Frontend (.env)
```env
REACT_APP_API_URL=http://localhost:8000/api
```

#### Backend (.env)
```env
PYTHONUNBUFFERED=1
DEVICE=cpu  # or "cuda" for GPU
LOG_LEVEL=INFO
HUGGINGFACE_API_KEY=your_key
OPENAI_API_KEY=your_key
```

### Settings File (config/settings.py)
- `EMBEDDING_MODEL`: Embedding model name
- `LLM_MODEL`: Language model
- `DEVICE`: Compute device
- `TOP_K_DOCUMENTS`: Documents to retrieve
- Multilingual settings

## Docker Deployment

### Build Images
```bash
# Build all services
docker-compose build

# Build specific service
docker-compose build frontend
docker-compose build backend
```

### Start Services
```bash
# Start in background
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Volume Mounts
- `./data` - Uploaded documents
- `./models` - FAISS indices
- `./logs` - Application logs

## Browser Compatibility

| Browser | Version | Status |
|---------|---------|--------|
| Chrome  | 90+     | ✅ Full support |
| Firefox | 88+     | ✅ Full support |
| Safari  | 14+     | ✅ Full support |
| Edge    | 90+     | ✅ Full support |

## Troubleshooting

### Frontend won't load
1. Check backend is running: `curl http://localhost:8000/api/health`
2. Check API URL in frontend `.env`
3. Clear browser cache

### Backend connection error
1. Verify backend service: `docker-compose logs backend`
2. Check port 8000 is open
3. Restart services: `docker-compose restart`

### Upload fails
1. Check file size (max 100MB)
2. Verify file format
3. Check logs for errors

### Out of memory
1. Use smaller embedding model
2. Reduce document batch size
3. Enable GPU acceleration

## Performance

### Optimization Tips
1. **Models**: Use smaller models for faster inference
2. **GPU**: Set `DEVICE=cuda` for GPU acceleration
3. **Caching**: Browser caches API responses
4. **Concurrency**: Deploy with multiple workers

### Typical Response Times
- Chat query: 1-3 seconds
- Document upload: 2-5 seconds
- Citation extraction: < 500ms
- Language detection: < 100ms

## Security

### For Production
1. Enable authentication (JWT)
2. Configure CORS properly
3. Use HTTPS
4. Add rate limiting
5. Validate file uploads
6. Use environment variables for secrets

## Next Steps

1. **Upload documents**: Use drag & drop in sidebar
2. **Ask questions**: Type in chat input
3. **View citations**: Click on citations in responses
4. **Adjust settings**: Configure in settings panel
5. **Save progress**: Click "Save Index" button

## Additional Resources

- [Frontend Documentation](frontend/README.md)
- [Backend API Documentation](backend/README.md)
- [Main README](README.md)
- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [React Documentation](https://react.dev/)

## Support

For issues or questions:
1. Check logs: `docker-compose logs`
2. Review documentation in README files
3. Test API endpoints: `http://localhost:8000/docs`

---

**Happy Chatting! 🤖**
