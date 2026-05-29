"""Test suite for RAG Chatbot."""
import pytest
from pathlib import Path
import sys

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.document_processor import DocumentProcessor
from src.embeddings import EmbeddingManager
from src.retriever import RAGRetriever
from src.summarizer import DocumentSummarizer
from src.citation_extractor import CitationExtractor
from src.multilingual import MultilingualHandler


class TestDocumentProcessor:
    """Test document processor."""
    
    def test_chunk_text(self):
        """Test text chunking."""
        processor = DocumentProcessor()
        text = "This is a test. " * 100
        chunks = processor.chunk_text(text)
        assert len(chunks) > 0
        assert all(isinstance(chunk, str) for chunk in chunks)


class TestEmbeddingManager:
    """Test embedding manager."""
    
    def test_initialization(self):
        """Test embedding manager initialization."""
        manager = EmbeddingManager(device="cpu")
        assert manager.embedding_dim > 0
        assert manager.index is None
    
    def test_add_texts(self):
        """Test adding texts."""
        manager = EmbeddingManager(device="cpu")
        texts = ["This is a test.", "Another test text."]
        manager.add_texts(texts)
        
        assert manager.index is not None
        assert len(manager.texts) == 2


class TestRetriever:
    """Test RAG retriever."""
    
    def test_initialization(self):
        """Test retriever initialization."""
        manager = EmbeddingManager(device="cpu")
        retriever = RAGRetriever(manager)
        assert retriever.top_k == 5


class TestSummarizer:
    """Test document summarizer."""
    
    def test_truncate_summary(self):
        """Test truncate fallback."""
        summarizer = DocumentSummarizer()
        text = "This is a test. " * 100
        summary = summarizer._truncate_summary(text, max_length=100)
        assert len(summary) > 0


class TestCitationExtractor:
    """Test citation extractor."""
    
    def test_extract_citations(self):
        """Test citation extraction."""
        extractor = CitationExtractor()
        text = "Check out https://example.com for more info. Also see doi:10.1234/example"
        citations = extractor.extract_citations(text)
        assert len(citations) >= 1


class TestMultilingualHandler:
    """Test multilingual handler."""
    
    def test_detect_language(self):
        """Test language detection."""
        handler = MultilingualHandler()
        result = handler.detect_language("Hello world")
        assert "language_code" in result
        assert result["language_code"] in ["en", "es"]  # May vary


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
