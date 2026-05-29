"""Example script showing RAG Chatbot usage."""
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.rag_chatbot import MultimodalRAGChatbot
from config.settings import EMBEDDING_MODEL, LLM_MODEL, DEVICE

def main():
    """Example usage of RAG Chatbot."""
    
    print("Initializing Multimodal RAG Chatbot...")
    chatbot = MultimodalRAGChatbot(
        embedding_model=EMBEDDING_MODEL,
        llm_model=LLM_MODEL,
        device=DEVICE
    )
    
    print("✅ Chatbot initialized successfully\n")
    
    # Example: Add a sample document
    print("Adding sample documents...")
    
    # Create a sample text file
    sample_text = """
    Machine Learning is a subset of Artificial Intelligence that focuses on the development 
    of algorithms and statistical models that enable computers to improve their performance 
    on tasks through experience.
    
    The main categories of Machine Learning are:
    1. Supervised Learning: Learning from labeled data
    2. Unsupervised Learning: Finding patterns in unlabeled data
    3. Reinforcement Learning: Learning through interaction and rewards
    
    Applications include computer vision, natural language processing, and predictive analytics.
    """
    
    with open("sample_document.txt", "w") as f:
        f.write(sample_text)
    
    result = chatbot.add_document("sample_document.txt")
    print(f"✅ Added document: {result['file_name']}")
    print(f"   Chunks: {result['chunks_added']}\n")
    
    # Example questions
    questions = [
        "What is Machine Learning?",
        "What are the main categories of ML?",
        "What are applications of Machine Learning?"
    ]
    
    print("Answering questions...\n")
    print("=" * 80)
    
    for question in questions:
        print(f"\n❓ Question: {question}")
        
        result = chatbot.answer_question(
            question,
            include_summary=True,
            language=None
        )
        
        print(f"✅ Answer: {result['answer']}")
        
        if result.get("citations"):
            print(f"\n📚 Citations found: {len(result['citations'])}")
        
        if result.get("summary"):
            print(f"\n📝 Summary: {result['summary']}")
        
        print("-" * 80)
    
    # Print statistics
    print("\n📊 Chatbot Statistics:")
    stats = chatbot.get_stats()
    print(f"Total Documents: {stats['total_documents']}")
    print(f"Embedding Dimension: {stats['embedding_dim']}")
    print(f"Chat History: {stats['chat_history_length']}")
    
    # Save index
    print("\n💾 Saving index...")
    chatbot.save_index("models/example_index")
    print("✅ Index saved")
    
    # Cleanup
    Path("sample_document.txt").unlink()


if __name__ == "__main__":
    main()
