"""Main RAG Chatbot application."""
import logging
from typing import Optional, Dict, List
from pathlib import Path
from .document_processor import DocumentProcessor
from .embeddings import EmbeddingManager
from .retriever import RAGRetriever
from .summarizer import DocumentSummarizer
from .citation_extractor import CitationExtractor
from .multilingual import MultilingualHandler
from .llm_interface import LLMInterface

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MultimodalRAGChatbot:
    """Main Multimodal RAG Chatbot application."""

    def __init__(
        self,
        embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2",
        llm_model: str = "gpt2",
        device: str = "cpu",
        index_path: Optional[str] = None
    ):
        """Initialize RAG Chatbot.
        
        Args:
            embedding_model: Embedding model name
            llm_model: LLM model name
            device: Device to use
            index_path: Path to existing FAISS index
        """
        self.device = device
        
        # Initialize components
        self.document_processor = DocumentProcessor()
        self.embedding_manager = EmbeddingManager(embedding_model, device=device)
        self.retriever = RAGRetriever(self.embedding_manager, top_k=5)
        self.summarizer = DocumentSummarizer(device=0 if device == "cuda" else -1)
        self.citation_extractor = CitationExtractor()
        self.multilingual_handler = MultilingualHandler()
        self.llm = LLMInterface(llm_model, device=0 if device == "cuda" else -1)
        
        # Load existing index if provided
        if index_path and Path(index_path).exists():
            self.load_index(index_path)
        
        self.chat_history = []
        logger.info("RAG Chatbot initialized successfully")

    def add_document(self, document_path: str, document_type: Optional[str] = None) -> Dict:
        """Add document to the chatbot.
        
        Args:
            document_path: Path to document
            document_type: Type of document (pdf, image, text)
            
        Returns:
            Dictionary with processing results
        """
        try:
            logger.info(f"Processing document: {document_path}")
            
            # Determine document type
            if document_type is None:
                suffix = Path(document_path).suffix.lower()
                if suffix == ".pdf":
                    document_type = "pdf"
                elif suffix in [".jpg", ".jpeg", ".png", ".gif"]:
                    document_type = "image"
                else:
                    document_type = "text"
            
            # Process document
            if document_type == "pdf":
                doc_data = self.document_processor.process_pdf(document_path)
            elif document_type == "image":
                doc_data = self.document_processor.process_image(document_path)
            else:
                doc_data = self.document_processor.process_text_file(document_path)
            
            # Extract text
            text = doc_data["text"]
            
            # Chunk text
            chunks = self.document_processor.chunk_text(text)
            
            # Create metadata
            metadata = [
                {
                    "source": doc_data["file_name"],
                    "chunk": i,
                    "document_type": document_type,
                    **doc_data["metadata"]
                }
                for i in range(len(chunks))
            ]
            
            # Add to embeddings
            self.embedding_manager.add_texts(chunks, metadata)
            
            result = {
                "status": "success",
                "file_name": doc_data["file_name"],
                "chunks_added": len(chunks),
                "total_documents": self.embedding_manager.get_index_stats()["total_documents"]
            }
            
            logger.info(f"Document added successfully. Total chunks: {len(chunks)}")
            return result
        except Exception as e:
            logger.error(f"Error adding document: {str(e)}")
            return {"status": "error", "message": str(e)}

    def answer_question(
        self,
        question: str,
        max_context_length: int = 2000,
        include_summary: bool = False,
        language: Optional[str] = None
    ) -> Dict:
        """Answer question using RAG.
        
        Args:
            question: User question
            max_context_length: Maximum context length
            include_summary: Whether to include document summary
            language: Language of question (auto-detect if None)
            
        Returns:
            Dictionary with answer and metadata
        """
        try:
            logger.info(f"Answering question: {question}")
            
            # Handle multilingual query
            if language is None:
                multilingual_result = self.multilingual_handler.process_multilingual_query(question)
                processed_question = multilingual_result["translated_query"]
                original_language = multilingual_result["original_language"]
            else:
                processed_question = self.multilingual_handler.translate(question, target_lang="en")
                original_language = self.multilingual_handler.detect_language(question)
            
            # Retrieve context
            context = self.retriever.get_context(processed_question, max_context_length)
            
            # Extract citations
            citations = self.citation_extractor.extract_citations(context)
            
            # Generate response
            response = self.llm.generate_rag_response(
                processed_question,
                context,
                max_length=512,
                temperature=0.7
            )
            
            # Summarize retrieved documents if requested
            summary = None
            if include_summary and len(context) > 0:
                summary = self.summarizer.summarize(context, max_length=150)
            
            # Store in chat history
            self.chat_history.append({
                "question": question,
                "answer": response,
                "citations": citations,
                "language": original_language
            })
            
            return {
                "question": question,
                "answer": response,
                "citations": citations,
                "summary": summary,
                "original_language": original_language["language_code"],
                "retrieved_documents": len(self.retriever.retrieve(processed_question))
            }
        except Exception as e:
            logger.error(f"Error answering question: {str(e)}")
            return {"error": str(e)}

    def get_chat_history(self) -> List[Dict]:
        """Get chat history.
        
        Returns:
            List of chat messages
        """
        return self.chat_history.copy()

    def clear_chat_history(self) -> None:
        """Clear chat history."""
        self.chat_history = []
        logger.info("Chat history cleared")

    def save_index(self, save_path: str) -> None:
        """Save FAISS index.
        
        Args:
            save_path: Path to save index
        """
        self.embedding_manager.save_index(save_path)
        logger.info(f"Index saved to {save_path}")

    def load_index(self, load_path: str) -> None:
        """Load FAISS index.
        
        Args:
            load_path: Path to load index from
        """
        self.embedding_manager.load_index(load_path)
        logger.info(f"Index loaded from {load_path}")

    def get_stats(self) -> Dict:
        """Get chatbot statistics.
        
        Returns:
            Dictionary with statistics
        """
        stats = self.embedding_manager.get_index_stats()
        stats["chat_history_length"] = len(self.chat_history)
        return stats
