"""Streamlit web interface for RAG Chatbot."""
import streamlit as st
from pathlib import Path
import sys
import logging

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.rag_chatbot import MultimodalRAGChatbot
from config.settings import (
    EMBEDDING_MODEL,
    LLM_MODEL,
    DEVICE,
    STREAMLIT_PAGE_TITLE,
    STREAMLIT_PAGE_ICON,
    FAISS_INDEX_PATH
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Page configuration
st.set_page_config(
    page_title=STREAMLIT_PAGE_TITLE,
    page_icon=STREAMLIT_PAGE_ICON,
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        padding: 10px;
        font-weight: bold;
    }
    .assistant-message {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    .user-message {
        background-color: #e8f4f8;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    </style>
""", unsafe_allow_html=True)


@st.cache_resource
def initialize_chatbot():
    """Initialize chatbot (cached to avoid reloading)."""
    try:
        chatbot = MultimodalRAGChatbot(
            embedding_model=EMBEDDING_MODEL,
            llm_model=LLM_MODEL,
            device=DEVICE,
            index_path=str(FAISS_INDEX_PATH) if FAISS_INDEX_PATH.exists() else None
        )
        return chatbot
    except Exception as e:
        st.error(f"Failed to initialize chatbot: {str(e)}")
        return None


def main():
    """Main Streamlit app."""
    st.title(f"{STREAMLIT_PAGE_ICON} {STREAMLIT_PAGE_TITLE}")
    
    # Initialize chatbot
    chatbot = initialize_chatbot()
    if chatbot is None:
        st.stop()
    
    # Sidebar
    with st.sidebar:
        st.header("📋 Settings")
        
        # Statistics
        stats = chatbot.get_stats()
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total Documents", stats.get("total_documents", 0))
        with col2:
            st.metric("Chat History", stats.get("chat_history_length", 0))
        
        st.divider()
        
        # Document upload
        st.subheader("📄 Upload Documents")
        uploaded_files = st.file_uploader(
            "Upload PDF, Image, or Text files",
            type=["pdf", "txt", "jpg", "jpeg", "png", "gif"],
            accept_multiple_files=True
        )
        
        if uploaded_files:
            for uploaded_file in uploaded_files:
                # Save temporarily
                temp_path = Path(f"temp_{uploaded_file.name}")
                with open(temp_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                
                # Process
                with st.spinner(f"Processing {uploaded_file.name}..."):
                    result = chatbot.add_document(str(temp_path))
                    if result.get("status") == "success":
                        st.success(f"✅ Added {result['chunks_added']} chunks")
                    else:
                        st.error(f"Error: {result.get('message', 'Unknown error')}")
                
                # Clean up
                temp_path.unlink()
        
        st.divider()
        
        # Options
        st.subheader("⚙️ Options")
        include_summary = st.checkbox("Include Document Summary", value=False)
        language = st.selectbox(
            "Query Language",
            options=["Auto-detect"] + list(chatbot.multilingual_handler.get_supported_languages().keys())
        )
        
        selected_language = None if language == "Auto-detect" else language
        
        st.divider()
        
        # Chat history
        st.subheader("💬 Chat History")
        if st.button("Clear History"):
            chatbot.clear_chat_history()
            st.success("Chat history cleared")
        
        # Save index
        if st.button("Save Index"):
            chatbot.save_index(str(FAISS_INDEX_PATH))
            st.success("Index saved")
    
    # Main chat area
    st.subheader("🤖 Ask a Question")
    
    # Display chat history
    for message in chatbot.get_chat_history():
        with st.container():
            st.markdown("**You:**")
            st.markdown(f'<div class="user-message">{message["question"]}</div>', unsafe_allow_html=True)
            
            st.markdown("**Assistant:**")
            st.markdown(f'<div class="assistant-message">{message["answer"]}</div>', unsafe_allow_html=True)
            
            # Citations
            if message.get("citations"):
                with st.expander("📚 Citations"):
                    for i, citation in enumerate(message["citations"], 1):
                        if "url" in citation:
                            st.markdown(f"[{i}. {citation['full_match']}]({citation['url']})")
                        else:
                            st.write(f"{i}. {citation}")
    
    # Input area
    col1, col2 = st.columns([4, 1])
    with col1:
        user_input = st.text_input("Your question:", placeholder="Ask a question about your documents...")
    with col2:
        submit_button = st.button("Send", use_container_width=True)
    
    if submit_button and user_input:
        with st.spinner("Thinking..."):
            result = chatbot.answer_question(
                user_input,
                include_summary=include_summary,
                language=selected_language
            )
            
            if "error" in result:
                st.error(f"Error: {result['error']}")
            else:
                # Display new response
                st.markdown("**You:**")
                st.markdown(f'<div class="user-message">{result["question"]}</div>', unsafe_allow_html=True)
                
                st.markdown("**Assistant:**")
                st.markdown(f'<div class="assistant-message">{result["answer"]}</div>', unsafe_allow_html=True)
                
                # Summary
                if result.get("summary"):
                    with st.expander("📝 Summary"):
                        st.write(result["summary"])
                
                # Citations
                if result.get("citations"):
                    with st.expander("📚 Citations"):
                        for i, citation in enumerate(result["citations"], 1):
                            if "url" in citation:
                                st.markdown(f"[{i}. {citation['full_match']}]({citation['url']})")
                            else:
                                st.write(f"{i}. {citation}")
                
                # Metadata
                with st.expander("ℹ️ Details"):
                    st.write(f"Language: {result['original_language']}")
                    st.write(f"Retrieved Documents: {result['retrieved_documents']}")
        
        st.rerun()


if __name__ == "__main__":
    main()
