"""Document summarization module."""
import logging
from typing import List, Optional
from transformers import pipeline
from langchain.text_splitter import RecursiveCharacterTextSplitter

logger = logging.getLogger(__name__)


class DocumentSummarizer:
    """Summarize documents using transformer models."""

    def __init__(self, model_name: str = "facebook/bart-large-cnn", device: int = -1):
        """Initialize summarizer.
        
        Args:
            model_name: Hugging Face model name for summarization
            device: Device to use (0 for GPU, -1 for CPU)
        """
        self.model_name = model_name
        self.device = device
        
        try:
            self.summarizer = pipeline(
                "summarization",
                model=model_name,
                device=device
            )
        except Exception as e:
            logger.warning(f"Failed to load summarizer: {str(e)}. Using fallback.")
            self.summarizer = None

    def summarize(self, text: str, max_length: int = 150, min_length: int = 50) -> str:
        """Summarize text.
        
        Args:
            text: Text to summarize
            max_length: Maximum summary length
            min_length: Minimum summary length
            
        Returns:
            Summarized text
        """
        if not self.summarizer:
            logger.warning("Summarizer not available. Returning text truncation.")
            return self._truncate_summary(text, max_length)
        
        try:
            # Handle long documents by chunking
            if len(text.split()) > 1024:
                return self._summarize_long_document(text, max_length, min_length)
            
            # Summarize
            summary = self.summarizer(
                text,
                max_length=max_length,
                min_length=min_length,
                do_sample=False
            )
            
            return summary[0]["summary_text"]
        except Exception as e:
            logger.error(f"Error summarizing text: {str(e)}")
            return self._truncate_summary(text, max_length)

    def _summarize_long_document(self, text: str, max_length: int, min_length: int) -> str:
        """Summarize long documents by chunking."""
        try:
            splitter = RecursiveCharacterTextSplitter(
                chunk_size=512,
                chunk_overlap=50,
                separators=["\n\n", "\n", " ", ""]
            )
            chunks = splitter.split_text(text)
            
            # Summarize each chunk
            summaries = []
            for chunk in chunks[:5]:  # Limit to first 5 chunks
                if chunk.strip():
                    try:
                        summary = self.summarizer(
                            chunk,
                            max_length=max_length // len(chunks[:5]),
                            min_length=min(min_length // len(chunks[:5]), 30),
                            do_sample=False
                        )
                        summaries.append(summary[0]["summary_text"])
                    except Exception as e:
                        logger.warning(f"Failed to summarize chunk: {str(e)}")
            
            # Combine summaries
            combined = " ".join(summaries)
            return combined
        except Exception as e:
            logger.error(f"Error summarizing long document: {str(e)}")
            return self._truncate_summary(text, max_length)

    def _truncate_summary(self, text: str, max_length: int) -> str:
        """Fallback: truncate text to approximate length."""
        words = text.split()
        truncated = " ".join(words[:max_length // 5])  # Approximate word count
        if len(words) > max_length // 5:
            truncated += "..."
        return truncated

    def extract_key_points(self, text: str, num_points: int = 5) -> List[str]:
        """Extract key points from text using sentence scoring."""
        try:
            from transformers import pipeline
            
            # Use zero-shot classification for key point extraction
            classifier = pipeline("zero-shot-classification", device=self.device)
            
            sentences = text.split(".")
            sentences = [s.strip() for s in sentences if s.strip()]
            
            if len(sentences) > num_points:
                # Score sentences by relevance
                scores = []
                for sentence in sentences[:20]:  # Limit to first 20
                    result = classifier(sentence, ["main topic", "detail"])
                    scores.append(result["scores"][0])
                
                # Get top sentences
                top_indices = sorted(
                    range(len(scores)),
                    key=lambda i: scores[i],
                    reverse=True
                )[:num_points]
                
                key_points = [sentences[i] + "." for i in sorted(top_indices)]
                return key_points
            else:
                return [s + "." for s in sentences[:num_points]]
        except Exception as e:
            logger.warning(f"Error extracting key points: {str(e)}")
            # Fallback: return first sentences
            sentences = text.split(".")
            return [s.strip() + "." for s in sentences[:num_points] if s.strip()]
