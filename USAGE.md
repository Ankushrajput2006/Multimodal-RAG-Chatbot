# RAG Chatbot Example Usage

This notebook demonstrates how to use the Multimodal RAG Chatbot.

## Quick Start

```python
from src.rag_chatbot import MultimodalRAGChatbot

# Initialize
chatbot = MultimodalRAGChatbot()

# Add documents
chatbot.add_document("example.pdf")
chatbot.add_document("image.png")

# Ask questions
result = chatbot.answer_question("What's the main topic?")
print(result["answer"])
```

## Advanced Usage

### With Custom Settings

```python
from src.rag_chatbot import MultimodalRAGChatbot

chatbot = MultimodalRAGChatbot(
    embedding_model="sentence-transformers/all-mpnet-base-v2",
    llm_model="distilgpt2",
    device="cuda"
)
```

### Multilingual Queries

```python
# Spanish query
result = chatbot.answer_question(
    "¿Cuáles son los hallazgos principales?",
    language="es"
)

# Auto-detect language
result = chatbot.answer_question(
    "Qu'est-ce que c'est?",
    language=None  # Auto-detected as French
)
```

### With Citations

```python
result = chatbot.answer_question("What's the research method?")

print("Answer:", result["answer"])
print("\nCitations:")
for i, citation in enumerate(result["citations"], 1):
    if "url" in citation:
        print(f"{i}. {citation['full_match']}: {citation['url']}")
```

## See Also

- [README.md](README.md) - Main documentation
- [tests/](tests/) - Unit tests
