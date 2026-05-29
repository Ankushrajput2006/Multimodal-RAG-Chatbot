"""Embedding generation and management."""
import logging
from typing import List, Optional, Tuple
import numpy as np
from sentence_transformers import SentenceTransformer
import faiss
import pickle
from pathlib import Path

logger = logging.getLogger(__name__)


class EmbeddingManager:
    """Manage embeddings and FAISS index."""

    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2", device: str = "cpu"):
        """Initialize embedding manager.
        
        Args:
            model_name: Hugging Face model name for embeddings
            device: Device to use ("cpu" or "cuda")
        """
        self.model_name = model_name
        self.device = device
        self.model = SentenceTransformer(model_name, device=device)
        self.embedding_dim = self.model.get_sentence_embedding_dimension()
        
        self.index = None
        self.texts = []
        self.metadata = []
        self.index_path = None

    def add_texts(self, texts: List[str], metadata: Optional[List[dict]] = None) -> None:
        """Add texts to index.
        
        Args:
            texts: List of text strings to embed
            metadata: Optional metadata for each text
        """
        try:
            logger.info(f"Generating embeddings for {len(texts)} texts...")
            embeddings = self.model.encode(texts, convert_to_numpy=True)
            
            if self.index is None:
                self.index = faiss.IndexFlatL2(self.embedding_dim)
            
            self.index.add(embeddings.astype('float32'))
            self.texts.extend(texts)
            
            if metadata:
                self.metadata.extend(metadata)
            else:
                self.metadata.extend([{"index": i} for i in range(len(texts))])
            
            logger.info(f"Index updated. Total documents: {len(self.texts)}")
        except Exception as e:
            logger.error(f"Error adding texts to index: {str(e)}")
            raise

    def search(self, query: str, k: int = 5) -> List[Tuple[str, float, dict]]:
        """Search for similar documents.
        
        Args:
            query: Query text
            k: Number of results to return
            
        Returns:
            List of (text, score, metadata) tuples
        """
        try:
            if self.index is None or len(self.texts) == 0:
                logger.warning("Index is empty. No results to return.")
                return []
            
            # Encode query
            query_embedding = self.model.encode([query], convert_to_numpy=True).astype('float32')
            
            # Search
            distances, indices = self.index.search(query_embedding, min(k, len(self.texts)))
            
            # Process results
            results = []
            for idx, distance in zip(indices[0], distances[0]):
                if idx < len(self.texts):
                    # Convert L2 distance to similarity score (0-1)
                    similarity = 1 / (1 + distance)
                    results.append((
                        self.texts[idx],
                        similarity,
                        self.metadata[idx] if idx < len(self.metadata) else {}
                    ))
            
            return results
        except Exception as e:
            logger.error(f"Error searching index: {str(e)}")
            return []

    def save_index(self, save_path: str) -> None:
        """Save FAISS index and metadata.
        
        Args:
            save_path: Directory to save index
        """
        try:
            save_dir = Path(save_path)
            save_dir.mkdir(parents=True, exist_ok=True)
            
            if self.index is not None:
                faiss.write_index(self.index, str(save_dir / "index.faiss"))
                logger.info(f"FAISS index saved to {save_dir / 'index.faiss'}")
            
            # Save metadata
            metadata_dict = {
                "texts": self.texts,
                "metadata": self.metadata,
                "embedding_dim": self.embedding_dim,
                "model_name": self.model_name
            }
            
            with open(save_dir / "metadata.pkl", 'wb') as f:
                pickle.dump(metadata_dict, f)
            logger.info(f"Metadata saved to {save_dir / 'metadata.pkl'}")
            
            self.index_path = save_dir
        except Exception as e:
            logger.error(f"Error saving index: {str(e)}")
            raise

    def load_index(self, load_path: str) -> None:
        """Load FAISS index and metadata.
        
        Args:
            load_path: Directory containing saved index
        """
        try:
            load_dir = Path(load_path)
            
            # Load FAISS index
            index_file = load_dir / "index.faiss"
            if index_file.exists():
                self.index = faiss.read_index(str(index_file))
                logger.info(f"FAISS index loaded from {index_file}")
            
            # Load metadata
            metadata_file = load_dir / "metadata.pkl"
            if metadata_file.exists():
                with open(metadata_file, 'rb') as f:
                    metadata_dict = pickle.load(f)
                    self.texts = metadata_dict["texts"]
                    self.metadata = metadata_dict["metadata"]
                    self.embedding_dim = metadata_dict["embedding_dim"]
                logger.info(f"Metadata loaded from {metadata_file}")
            
            self.index_path = load_dir
        except Exception as e:
            logger.error(f"Error loading index: {str(e)}")
            raise

    def get_index_stats(self) -> dict:
        """Get index statistics."""
        return {
            "total_documents": len(self.texts),
            "embedding_dim": self.embedding_dim,
            "model_name": self.model_name,
            "index_size": self.index.ntotal if self.index else 0
        }
