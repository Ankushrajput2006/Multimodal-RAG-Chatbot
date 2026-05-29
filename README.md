# Multimodal RAG Chatbot

A Retrieval-Augmented Generation (RAG) chatbot capable of understanding and answering questions from PDFs, research papers, and images with multilingual support.

## Features

✨ **Core Features:**
- 📄 **PDF & Document Processing**: Extract text and metadata from PDFs
- 🖼️ **Image Understanding**: OCR support for images and scanned documents
- 🔍 **Semantic Search**: FAISS-based vector embeddings for intelligent retrieval
- 📝 **Document Summarization**: Automatic summaries of retrieved documents
- 🔗 **Citation Extraction**: Extract and format citations (APA, MLA, Chicago)
- 🌍 **Multilingual Support**: Query and document processing in multiple languages
- 💻 **Web UI**: Streamlit-based interactive interface
- 🐳 **Docker Deployment**: Containerized for scalable deployment

## Architecture

```
┌─────────────────────────────────────────┐
│         Streamlit Web Interface         │
├─────────────────────────────────────────┤
│                                         │
│  ┌──────────────────────────────────┐   │
│  │   MultimodalRAGChatbot (Main)    │   │
│  └──────────────────────────────────┘   │
│           ↓ ↓ ↓ ↓ ↓ ↓                    │
│  ┌────────────────────────────────┐     │
│  │ Document | Embedding | Retriever│     │
│  │ Processor| Manager  | & Ranker  │     │
│  └────────────────────────────────┘     │
│           ↓ ↓ ↓                          │
│  ┌────────────────────────────────┐     │
│  │ Summarizer | Citation | LLM    │     │
│  │ Extractor | Interface│          │     │
│  └────────────────────────────────┘     │
│           ↓ ↓ ↓                          │
│  ┌────────────────────────────────┐     │
│  │ FAISS Index | Language Detect  │     │
│  │ Vector Store| & Translator     │     │
│  └────────────────────────────────┘     │
└─────────────────────────────────────────┘
```

## Installation

### Prerequisites
- Python 3.10+
- GPU support (CUDA) optional but recommended
- Docker & Docker Compose (for containerized deployment)

### Local Setup

1. **Clone the repository**
```bash
cd "c:\Users\ankus\Documents\multi model rag chatbot"
```

2. **Create virtual environment**
```bash
python -m venv venv
venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Download Tesseract OCR** (for image processing)
   - Windows: Download installer from https://github.com/UB-Mannheim/tesseract/wiki
   - Linux: `sudo apt-get install tesseract-ocr`
   - macOS: `brew install tesseract`

5. **Run the application**
```bash
streamlit run app.py
```

The app will be available at `http://localhost:8501`

### Docker Deployment

1. **Build and run with Docker Compose**
```bash
docker-compose up -d
```

2. **Access the application**
```
http://localhost:8501
```

## Usage

### Basic Usage

```python
from src.rag_chatbot import MultimodalRAGChatbot

# Initialize chatbot
chatbot = MultimodalRAGChatbot(
    embedding_model="sentence-transformers/all-MiniLM-L6-v2",
    llm_model="gpt2",
    device="cpu"
)

# Add documents
result = chatbot.add_document("research_paper.pdf")
print(f"Added {result['chunks_added']} chunks")

# Ask questions
answer = chatbot.answer_question(
    "What are the main findings?",
    include_summary=True,
    language="en"
)
print(answer["answer"])
print("Citations:", answer["citations"])
```

### Web Interface

1. **Upload Documents**: Use the sidebar to upload PDFs, images, or text files
2. **Ask Questions**: Type questions in the input field
3. **View Results**: See answers with citations and summaries
4. **Export**: Save the FAISS index for later use

## Project Structure

```
multi model rag chatbot/
├── src/
│   ├── __init__.py
│   ├── document_processor.py    # PDF/Image/Text processing
│   ├── embeddings.py            # FAISS embeddings manager
│   ├── retriever.py             # RAG retriever
│   ├── summarizer.py            # Document summarization
│   ├── citation_extractor.py    # Citation extraction & formatting
│   ├── multilingual.py          # Multilingual support
│   ├── llm_interface.py         # LLM interface
│   └── rag_chatbot.py           # Main chatbot class
├── config/
│   └── settings.py              # Configuration settings
├── data/                        # Document storage
├── models/                      # FAISS indices & models
├── logs/                        # Application logs
├── tests/
│   └── test_rag.py             # Unit tests
├── app.py                       # Streamlit web app
├── requirements.txt             # Python dependencies
├── Dockerfile                   # Docker configuration
├── docker-compose.yml          # Docker Compose setup
└── README.md                   # This file
```

## Configuration

Edit `config/settings.py` to customize:

- **Embedding Model**: Change `EMBEDDING_MODEL`
- **LLM Model**: Change `LLM_MODEL`
- **Device**: Set `DEVICE` to "cuda" or "cpu"
- **Languages**: Modify `SUPPORTED_LANGUAGES`
- **Citation Style**: Set `DEFAULT_CITATION_STYLE`

## Technologies Used

- **LangChain**: LLM framework and text processing
- **FAISS**: Vector similarity search
- **Sentence-Transformers**: Embedding models
- **Transformers (Hugging Face)**: LLM and NLP models
- **PyPDF2**: PDF text extraction
- **Pytesseract**: OCR for images
- **Streamlit**: Web interface
- **Docker**: Containerization
- **Deep Translator**: Multilingual translation
- **LangDetect**: Language detection

## API Reference

### MultimodalRAGChatbot

```python
# Add document
result = chatbot.add_document(
    document_path: str,
    document_type: Optional[str] = None
) -> Dict

# Answer question
result = chatbot.answer_question(
    question: str,
    max_context_length: int = 2000,
    include_summary: bool = False,
    language: Optional[str] = None
) -> Dict

# Save/Load index
chatbot.save_index(save_path: str) -> None
chatbot.load_index(load_path: str) -> None

# Get statistics
stats = chatbot.get_stats() -> Dict
```

## Performance Tips

1. **GPU Acceleration**: Set `DEVICE="cuda"` for faster inference
2. **Model Selection**: Use smaller models for faster processing
   - Embeddings: `all-MiniLM-L6-v2` (recommended for speed)
   - LLM: `distilgpt2` instead of `gpt2`
3. **Batch Processing**: Process multiple documents at once
4. **Index Caching**: Save and reuse FAISS indices

## Troubleshooting

**Issue**: OCR not working
- **Solution**: Ensure Tesseract is installed and in PATH

**Issue**: Out of memory
- **Solution**: Use `DEVICE="cpu"` or choose smaller models

**Issue**: Slow inference
- **Solution**: Use GPU acceleration or reduce context length

**Issue**: Poor retrieval quality
- **Solution**: Add more documents or use better embedding models

## Future Enhancements

- [ ] Support for tables and structured data extraction
- [ ] Custom fine-tuned embedding models
- [ ] Multi-modal embeddings (text + image)
- [ ] User authentication and document permissions
- [ ] REST API for integration
- [ ] Advanced RAG techniques (HyDE, Self-RAG)
- [ ] Real-time document indexing
- [ ] Analytics and usage tracking

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see LICENSE file for details.

## Citation

If you use this project in your research, please cite:

```bibtex
@software{rag_chatbot_2024,
  title={Multimodal RAG Chatbot},
  author={Your Name},
  year={2024},
  url={https://github.com/yourusername/multimodal-rag-chatbot}
}
```

## Contact

For questions and feedback, please contact: your.email@example.com

## Acknowledgments

- Hugging Face for transformer models and datasets
- Meta for FAISS library
- OpenAI for inspiration from ChatGPT
- Streamlit for the web framework

---

**Built with ❤️ using LangChain, FAISS, and Hugging Face**
