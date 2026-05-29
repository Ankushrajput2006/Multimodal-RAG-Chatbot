"""Configuration settings for RAG Chatbot."""
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Paths
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
MODELS_DIR = BASE_DIR / "models"
LOGS_DIR = BASE_DIR / "logs"

# Create directories if they don't exist
DATA_DIR.mkdir(exist_ok=True)
MODELS_DIR.mkdir(exist_ok=True)
LOGS_DIR.mkdir(exist_ok=True)

# Model Configuration
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
LLM_MODEL = "gpt2"  # Can be replaced with other HF models
DEVICE = "cuda"  # or "cpu"

# FAISS Configuration
FAISS_INDEX_PATH = MODELS_DIR / "faiss_index"
EMBEDDING_DIMENSION = 384

# PDF Processing
MAX_PDF_SIZE_MB = 50
PDF_EXTRACT_IMAGES = True

# Semantic Search
TOP_K_DOCUMENTS = 5
SIMILARITY_THRESHOLD = 0.3

# Multilingual Support
SUPPORTED_LANGUAGES = ["en", "es", "fr", "de", "zh", "ja", "ar"]
DEFAULT_LANGUAGE = "en"

# API Keys (load from environment)
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY", "")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

# Logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FILE = LOGS_DIR / "rag_chatbot.log"

# Streamlit Configuration
STREAMLIT_PAGE_TITLE = "Multimodal RAG Chatbot"
STREAMLIT_PAGE_ICON = "🤖"
STREAMLIT_LAYOUT = "wide"
STREAMLIT_INITIAL_SIDEBAR_STATE = "expanded"

# Citation Configuration
EXTRACT_CITATIONS = True
CITATION_STYLES = ["APA", "MLA", "Chicago"]
DEFAULT_CITATION_STYLE = "APA"
