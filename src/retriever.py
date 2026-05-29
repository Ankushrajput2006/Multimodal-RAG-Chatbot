"""Retrieval-Augmented Generation (RAG) retriever."""
import logging
from typing import List, Optional, Dict, Tuple
from .embeddings import EmbeddingManager

logger = logging.getLogger(__name__)


class RAGRetriever:
    """Retrieve relevant documents for generating responses."""

    def __init__(self, embedding_manager: EmbeddingManager, top_k: int = 5):
        """Initialize RAG retriever.
        
        Args:
            embedding_manager: EmbeddingManager instance
            top_k: Number of documents to retrieve
        """
        self.embedding_manager = embedding_manager
        self.top_k = top_k

    def retrieve(self, query: str, filters: Optional[Dict] = None) -> List[Tuple[str, float, dict]]:
        """Retrieve relevant documents for a query.
        
        Args:
            query: Query string
            filters: Optional filters to apply
            
        Returns:
            List of (text, similarity_score, metadata) tuples
        """
        try:
            # Search for similar documents
            results = self.embedding_manager.search(query, k=self.top_k)
            
            # Apply filters if provided
            if filters:
                results = self._apply_filters(results, filters)
            
            logger.info(f"Retrieved {len(results)} documents for query: {query[:100]}")
            return results
        except Exception as e:
            logger.error(f"Error retrieving documents: {str(e)}")
            return []

    def _apply_filters(self, results: List, filters: Dict) -> List:
        """Apply metadata filters to results.
        
        Args:
            results: List of (text, score, metadata) tuples
            filters: Dictionary of filters to apply
            
        Returns:
            Filtered results
        """
        filtered_results = []
        
        for text, score, metadata in results:
            include = True
            
            for key, value in filters.items():
                if key not in metadata:
                    include = False
                    break
                
                if isinstance(value, list):
                    if metadata[key] not in value:
                        include = False
                        break
                else:
                    if metadata[key] != value:
                        include = False
                        break
            
            if include:
                filtered_results.append((text, score, metadata))
        
        return filtered_results

    def get_context(self, query: str, max_context_length: int = 2000) -> str:
        """Get context string for LLM.
        
        Args:
            query: Query string
            max_context_length: Maximum context length
            
        Returns:
            Context string formatted for LLM
        """
        results = self.retrieve(query)
        
        context = "Retrieved Context:\n\n"
        current_length = 0
        
        for i, (text, score, metadata) in enumerate(results, 1):
            chunk = f"[Document {i}] (Relevance: {score:.2f})\n{text}\n\n"
            
            if current_length + len(chunk) <= max_context_length:
                context += chunk
                current_length += len(chunk)
            else:
                break
        
        return context

    def rerank_results(self, query: str, results: List, use_cross_encoder: bool = False) -> List:
        """Re-rank results using cross-encoder (optional).
        
        Args:
            query: Original query
            results: Initial results to re-rank
            use_cross_encoder: Whether to use cross-encoder for re-ranking
            
        Returns:
            Re-ranked results
        """
        if not use_cross_encoder or len(results) <= 1:
            return results
        
        try:
            from sentence_transformers import CrossEncoder
            
            model = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')
            
            # Prepare pairs for cross-encoder
            pairs = [[query, text] for text, _, _ in results]
            
            # Get scores
            scores = model.predict(pairs)
            
            # Re-rank
            ranked_results = [
                (text, float(score), metadata)
                for (text, _, metadata), score in zip(results, scores)
            ]
            ranked_results.sort(key=lambda x: x[1], reverse=True)
            
            return ranked_results
        except Exception as e:
            logger.warning(f"Cross-encoder re-ranking failed: {str(e)}. Returning original results.")
            return results
