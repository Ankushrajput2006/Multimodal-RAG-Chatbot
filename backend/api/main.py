"""FastAPI backend for RAG Chatbot."""
from fastapi import FastAPI, File, UploadFile, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import logging
import sys
from pathlib import Path
import tempfile
import uuid
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.rag_chatbot import MultimodalRAGChatbot
from config.settings import EMBEDDING_MODEL, LLM_MODEL, DEVICE, FAISS_INDEX_PATH
from backend.api.schemas import (
    ChatResponse, DocumentUploadResponse, ChatbotStats, LanguageInfo, ChatMessage
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI
app = FastAPI(
    title="Multimodal RAG Chatbot API",
    description="API for multimodal RAG chatbot with PDF, image, and text support",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize chatbot
try:
    chatbot = MultimodalRAGChatbot(
        embedding_model=EMBEDDING_MODEL,
        llm_model=LLM_MODEL,
        device=DEVICE,
        index_path=str(FAISS_INDEX_PATH) if FAISS_INDEX_PATH.exists() else None
    )
    logger.info("Chatbot initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize chatbot: {str(e)}")
    raise


# ============================================================================
# Health & Status Endpoints
# ============================================================================

@app.get("/api/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    }


@app.get("/api/stats", response_model=ChatbotStats)
async def get_stats():
    """Get chatbot statistics."""
    stats = chatbot.get_stats()
    return ChatbotStats(**stats)


# ============================================================================
# Chat Endpoints
# ============================================================================

@app.post("/api/chat", response_model=ChatResponse)
async def chat(
    question: str,
    include_summary: bool = False,
    language: str = None
):
    """Answer a question using RAG."""
    try:
        result = chatbot.answer_question(
            question=question,
            include_summary=include_summary,
            language=language
        )
        
        if "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])
        
        return ChatResponse(**result)
    except Exception as e:
        logger.error(f"Error in chat endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/chat-history")
async def get_chat_history():
    """Get chat history."""
    history = chatbot.get_chat_history()
    return {
        "messages": [
            ChatMessage(
                id=str(i),
                sender="user" if i % 2 == 0 else "assistant",
                content=msg.get("question") if i % 2 == 0 else msg.get("answer"),
                citations=msg.get("citations"),
                summary=msg.get("summary"),
                timestamp=datetime.now().isoformat()
            )
            for i, msg in enumerate(history)
        ]
    }


@app.delete("/api/chat-history")
async def clear_chat_history():
    """Clear chat history."""
    chatbot.clear_chat_history()
    return {"status": "success", "message": "Chat history cleared"}


# ============================================================================
# Document Endpoints
# ============================================================================

@app.post("/api/documents/upload", response_model=DocumentUploadResponse)
async def upload_document(file: UploadFile = File(...)):
    """Upload and process a document."""
    try:
        # Save temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=Path(file.filename).suffix) as tmp:
            tmp.write(await file.read())
            tmp_path = tmp.name
        
        # Process document
        result = chatbot.add_document(tmp_path)
        
        # Cleanup
        Path(tmp_path).unlink()
        
        if result.get("status") != "success":
            raise HTTPException(status_code=400, detail=result.get("message", "Upload failed"))
        
        return DocumentUploadResponse(**result)
    except Exception as e:
        logger.error(f"Error uploading document: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# Language Endpoints
# ============================================================================

@app.get("/api/languages")
async def get_supported_languages():
    """Get supported languages."""
    langs = chatbot.multilingual_handler.get_supported_languages()
    return {
        "languages": [
            {"code": code, "name": name}
            for code, name in langs.items()
        ]
    }


@app.post("/api/detect-language", response_model=LanguageInfo)
async def detect_language(text: str):
    """Detect language of text."""
    result = chatbot.multilingual_handler.detect_language(text)
    return LanguageInfo(**result)


# ============================================================================
# Settings Endpoints
# ============================================================================

@app.get("/api/settings")
async def get_settings():
    """Get current settings."""
    return {
        "embedding_model": EMBEDDING_MODEL,
        "llm_model": LLM_MODEL,
        "device": DEVICE,
        "supported_languages": list(chatbot.multilingual_handler.get_supported_languages().keys())
    }


# ============================================================================
# Index Management Endpoints
# ============================================================================

@app.post("/api/index/save")
async def save_index(background_tasks: BackgroundTasks):
    """Save FAISS index."""
    try:
        background_tasks.add_task(chatbot.save_index, str(FAISS_INDEX_PATH))
        return {"status": "success", "message": "Index save initiated"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/index/stats")
async def get_index_stats():
    """Get index statistics."""
    stats = chatbot.embedding_manager.get_index_stats()
    return stats


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
