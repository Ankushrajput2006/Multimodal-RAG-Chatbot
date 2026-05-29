"""Types for frontend-backend communication."""
from typing import Optional, List, Dict, Any
from pydantic import BaseModel


class DocumentMetadata(BaseModel):
    """Document metadata."""
    source: str
    chunk: int
    document_type: str
    num_pages: Optional[int] = None
    file_size: Optional[int] = None


class Citation(BaseModel):
    """Citation information."""
    type: str
    value: str
    full_match: str
    url: Optional[str] = None
    author: Optional[str] = None
    year: Optional[str] = None


class ChatMessage(BaseModel):
    """Chat message."""
    id: str
    sender: str  # "user" or "assistant"
    content: str
    citations: Optional[List[Citation]] = None
    summary: Optional[str] = None
    timestamp: str


class ChatResponse(BaseModel):
    """Response from chat API."""
    question: str
    answer: str
    citations: List[Citation]
    summary: Optional[str] = None
    original_language: str
    retrieved_documents: int


class DocumentUploadResponse(BaseModel):
    """Response from document upload."""
    status: str
    file_name: str
    chunks_added: int
    total_documents: int
    message: Optional[str] = None


class ChatbotStats(BaseModel):
    """Chatbot statistics."""
    total_documents: int
    embedding_dim: int
    chat_history_length: int
    model_name: Optional[str] = None


class LanguageInfo(BaseModel):
    """Language detection info."""
    language_code: str
    language_name: str
    confidence: float
