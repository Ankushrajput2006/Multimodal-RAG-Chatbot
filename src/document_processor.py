"""Document processing module for PDFs, images, and text."""
import logging
from pathlib import Path
from typing import List, Dict, Optional
import PyPDF2
from pdf2image import convert_from_path
import pytesseract
from PIL import Image
import cv2
import numpy as np
from langchain.text_splitter import RecursiveCharacterTextSplitter

logger = logging.getLogger(__name__)


class DocumentProcessor:
    """Process various document types (PDFs, images, text)."""

    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        """Initialize document processor.
        
        Args:
            chunk_size: Size of text chunks for splitting
            chunk_overlap: Overlap between chunks
        """
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=["\n\n", "\n", " ", ""]
        )

    def process_pdf(self, pdf_path: str) -> Dict[str, any]:
        """Extract text and images from PDF.
        
        Args:
            pdf_path: Path to PDF file
            
        Returns:
            Dictionary with extracted text and metadata
        """
        try:
            pdf_path = Path(pdf_path)
            if not pdf_path.exists():
                raise FileNotFoundError(f"PDF file not found: {pdf_path}")

            # Extract text
            text = self._extract_text_from_pdf(pdf_path)
            
            # Extract images
            images = self._extract_images_from_pdf(pdf_path)
            
            # Extract metadata
            metadata = self._extract_pdf_metadata(pdf_path)

            return {
                "text": text,
                "images": images,
                "metadata": metadata,
                "document_type": "pdf",
                "file_name": pdf_path.name
            }
        except Exception as e:
            logger.error(f"Error processing PDF {pdf_path}: {str(e)}")
            raise

    def process_image(self, image_path: str) -> Dict[str, any]:
        """Extract text from image using OCR.
        
        Args:
            image_path: Path to image file
            
        Returns:
            Dictionary with extracted text and image data
        """
        try:
            image_path = Path(image_path)
            if not image_path.exists():
                raise FileNotFoundError(f"Image file not found: {image_path}")

            # Load image
            img = Image.open(image_path)
            
            # OCR extraction
            text = pytesseract.image_to_string(img)
            
            # Convert to array for processing
            img_array = np.array(img)

            return {
                "text": text,
                "image": img_array,
                "metadata": {
                    "width": img.width,
                    "height": img.height,
                    "format": img.format
                },
                "document_type": "image",
                "file_name": image_path.name
            }
        except Exception as e:
            logger.error(f"Error processing image {image_path}: {str(e)}")
            raise

    def process_text_file(self, file_path: str) -> Dict[str, any]:
        """Process text file.
        
        Args:
            file_path: Path to text file
            
        Returns:
            Dictionary with text content
        """
        try:
            file_path = Path(file_path)
            if not file_path.exists():
                raise FileNotFoundError(f"Text file not found: {file_path}")

            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.read()

            return {
                "text": text,
                "metadata": {
                    "size": file_path.stat().st_size,
                    "encoding": "utf-8"
                },
                "document_type": "text",
                "file_name": file_path.name
            }
        except Exception as e:
            logger.error(f"Error processing text file {file_path}: {str(e)}")
            raise

    def chunk_text(self, text: str) -> List[str]:
        """Split text into chunks.
        
        Args:
            text: Text to split
            
        Returns:
            List of text chunks
        """
        return self.text_splitter.split_text(text)

    def _extract_text_from_pdf(self, pdf_path: Path) -> str:
        """Extract text from PDF using PyPDF2."""
        text = ""
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
        except Exception as e:
            logger.warning(f"Failed to extract text with PyPDF2: {str(e)}")
            # Fallback to OCR via images
            text = self._extract_text_via_ocr(pdf_path)
        
        return text

    def _extract_text_via_ocr(self, pdf_path: Path) -> str:
        """Extract text from PDF using OCR."""
        text = ""
        try:
            images = convert_from_path(pdf_path)
            for image in images:
                text += pytesseract.image_to_string(image) + "\n"
        except Exception as e:
            logger.error(f"OCR extraction failed: {str(e)}")
        return text

    def _extract_images_from_pdf(self, pdf_path: Path) -> List[np.ndarray]:
        """Extract images from PDF."""
        images = []
        try:
            pdf_images = convert_from_path(pdf_path)
            for img in pdf_images:
                images.append(np.array(img))
        except Exception as e:
            logger.warning(f"Failed to extract images: {str(e)}")
        return images

    def _extract_pdf_metadata(self, pdf_path: Path) -> Dict:
        """Extract PDF metadata."""
        metadata = {
            "file_size": pdf_path.stat().st_size,
            "file_name": pdf_path.name
        }
        
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                metadata["num_pages"] = len(pdf_reader.pages)
                if pdf_reader.metadata:
                    metadata.update({
                        "title": pdf_reader.metadata.get("/Title"),
                        "author": pdf_reader.metadata.get("/Author"),
                        "created": pdf_reader.metadata.get("/CreationDate")
                    })
        except Exception as e:
            logger.warning(f"Failed to extract PDF metadata: {str(e)}")
        
        return metadata
