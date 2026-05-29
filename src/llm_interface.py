"""LLM interface for RAG."""
import logging
from typing import Optional, List
from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
import torch

logger = logging.getLogger(__name__)


class LLMInterface:
    """Interface to Large Language Models for generation."""

    def __init__(self, model_name: str = "gpt2", device: int = -1):
        """Initialize LLM interface.
        
        Args:
            model_name: Model name or path
            device: Device to use (0 for GPU, -1 for CPU)
        """
        self.model_name = model_name
        self.device = device
        
        try:
            self.pipe = pipeline(
                "text-generation",
                model=model_name,
                device=device,
                torch_dtype=torch.float16 if device >= 0 else torch.float32
            )
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
            if self.tokenizer.pad_token is None:
                self.tokenizer.pad_token = self.tokenizer.eos_token
            
            logger.info(f"LLM loaded: {model_name}")
        except Exception as e:
            logger.error(f"Failed to load LLM: {str(e)}")
            raise

    def generate_response(
        self,
        prompt: str,
        context: Optional[str] = None,
        max_length: int = 512,
        temperature: float = 0.7,
        top_p: float = 0.9,
        num_return_sequences: int = 1
    ) -> str:
        """Generate response using LLM.
        
        Args:
            prompt: Input prompt
            context: Optional context to prepend
            max_length: Maximum response length
            temperature: Sampling temperature
            top_p: Top-p sampling parameter
            num_return_sequences: Number of sequences to generate
            
        Returns:
            Generated text
        """
        try:
            # Prepare input
            if context:
                full_prompt = f"Context:\n{context}\n\nQuestion: {prompt}\n\nAnswer:"
            else:
                full_prompt = prompt
            
            # Generate
            output = self.pipe(
                full_prompt,
                max_length=max_length,
                temperature=temperature,
                top_p=top_p,
                num_return_sequences=num_return_sequences,
                do_sample=True,
                pad_token_id=self.tokenizer.eos_token_id
            )
            
            # Extract generated text
            generated_text = output[0]["generated_text"]
            
            # Remove prompt from output
            response = generated_text[len(full_prompt):].strip()
            
            return response
        except Exception as e:
            logger.error(f"Error generating response: {str(e)}")
            return "Error generating response."

    def generate_rag_response(
        self,
        query: str,
        retrieved_context: str,
        system_prompt: Optional[str] = None,
        **kwargs
    ) -> str:
        """Generate RAG response using retrieved context.
        
        Args:
            query: User query
            retrieved_context: Retrieved context from documents
            system_prompt: Optional system prompt
            **kwargs: Additional arguments for generate_response
            
        Returns:
            Generated response
        """
        try:
            # Construct prompt
            if system_prompt:
                prompt = f"{system_prompt}\n\n{retrieved_context}\n\nQuestion: {query}\n\nAnswer:"
            else:
                prompt = f"{retrieved_context}\n\nQuestion: {query}\n\nAnswer:"
            
            response = self.generate_response(prompt, context=None, **kwargs)
            
            return response
        except Exception as e:
            logger.error(f"Error generating RAG response: {str(e)}")
            return "Unable to generate response."

    def get_model_info(self) -> dict:
        """Get model information.
        
        Returns:
            Dictionary with model info
        """
        return {
            "model_name": self.model_name,
            "device": "GPU" if self.device >= 0 else "CPU",
            "tokenizer": self.tokenizer.name_or_path if hasattr(self.tokenizer, 'name_or_path') else "Unknown"
        }
