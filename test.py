import streamlit as st
from utils import process_pdf, ask_pdf_question
import time


st.set_page_config(
    page_title="PDF Chatbot Pro",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Custom background gradient */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Main container styling */
    .main-container {
        background: rgba(255, 255, 255, 0.95);
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 8px 32px rgba(31, 38, 135, 0.37);
        backdrop-filter: blur(4px);
        border: 1px solid rgba(255, 255, 255, 0.18);
        margin: 1rem 1rem 1rem 0;
        max-width: 100%;
    }
    
    /* Chat message styling */
    .user-message {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 15px 20px;
        border-radius: 18px 18px 5px 18px;
        margin: 10px 0;
        max-width: 80%;
        margin-left: auto;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
        animation: slideInRight 0.3s ease-out;
    }
    
    .bot-message {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        color: white;
        padding: 15px 20px;
        border-radius: 18px 18px 18px 5px;
        margin: 10px 0;
        max-width: 80%;
        box-shadow: 0 4px 15px rgba(17, 153, 142, 0.3);
        animation: slideInLeft 0.3s ease-out;
    }
    
    /* Animations */
    @keyframes slideInRight {
        from { opacity: 0; transform: translateX(50px); }
        to { opacity: 1; transform: translateX(0); }
    }
    
    @keyframes slideInLeft {
        from { opacity: 0; transform: translateX(-50px); }
        to { opacity: 1; transform: translateX(0); }
    }
    
    /* Custom sidebar styling */
    .sidebar-content {
        background: rgba(255, 255, 255, 0.1);
        padding: 1rem;
        border-radius: 15px;
        margin-bottom: 1rem;
        backdrop-filter: blur(10px);
    }
    
    /* Upload area styling */
    .upload-section {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.1), rgba(255, 255, 255, 0.05));
        padding: 2rem;
        border-radius: 15px;
        border: 2px dashed rgba(255, 255, 255, 0.3);
        text-align: center;
        margin: 1rem 0;
        transition: all 0.3s ease;
    }
    
    .upload-section:hover {
        border-color: rgba(255, 255, 255, 0.6);
        background: rgba(255, 255, 255, 0.15);
    }
    
    /* Status indicators */
    .status-success {
        background: linear-gradient(90deg, #56ab2f, #a8e6cf);
        color: white;
        padding: 12px 20px;
        border-radius: 25px;
        text-align: center;
        margin: 15px 0;
        box-shadow: 0 4px 15px rgba(86, 171, 47, 0.3);
    }
    
    .status-processing {
        background: linear-gradient(90deg, #f093fb, #f5576c);
        color: white;
        padding: 12px 20px;
        border-radius: 25px;
        text-align: center;
        margin: 15px 0;
        box-shadow: 0 4px 15px rgba(240, 147, 251, 0.3);
    }
    
    /* Custom button styling */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 12px 30px;
        border-radius: 25px;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
    }
    
    /* Title styling */
    .main-title {
        text-align: center;
        color: #2c3e50;
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    
    .subtitle {
        text-align: center;
        color: #000000;
        font-size: 1.2rem;
        margin-bottom: 2rem;
        opacity: 0.8;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state for chat history
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

with st.sidebar:
    st.markdown('<div class="sidebar-content">', unsafe_allow_html=True)
    
    st.markdown("""
    <div style="text-align: center; padding: 1rem 0;">
        <h2 style="color: white; margin: 0;">📚 PDF Chatbot Pro</h2>
        <p style="color: rgba(255,255,255,0.8); font-size: 0.9rem; margin: 0.5rem 0;">
            Your intelligent document companion
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("""
    <div style="color: rgba(255,255,255,0.9); padding: 1rem 0;">
        <h4>✨ Features:</h4>
        <ul style="list-style-type: none; padding: 0;">
            <li>🔍 Smart PDF analysis</li>
            <li>💬 Natural conversations</li>
            <li>📝 Instant summaries</li>
            <li>🧠 AI-powered insights</li>
        </ul>
        
        
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    if st.button("🗑️ Clear Chat History", use_container_width=True):
        st.session_state.chat_history = []
        st.rerun()

# --- Main Content ---

st.markdown('<h1 class="main-title">📚 PDF Chatbot Pro</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Transform your PDFs into interactive conversations</p>', unsafe_allow_html=True)

# File upload section
st.markdown('<div class="upload-section">', unsafe_allow_html=True)
st.markdown("### 📎 Upload Your Document")

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    pdf = st.file_uploader(
        "Choose a PDF file",
        type=["pdf"],
        help="Upload a PDF document to start chatting with it",
        label_visibility="collapsed"
    )

st.markdown('</div>', unsafe_allow_html=True)

# Process PDF
knowledgeBase = None
if pdf:
    with st.spinner("🔄 Processing your PDF... This may take a moment"):
        progress_bar = st.progress(0)
        for i in range(100):
            time.sleep(0.01)
            progress_bar.progress(i + 1)
        
        knowledgeBase = process_pdf(pdf)
        progress_bar.empty()
    
    st.markdown(
        '<div class="status-success">✅ PDF processed successfully! You can now start chatting.</div>',
        unsafe_allow_html=True
    )
    
    # Display PDF info
    st.info(f"📄 **File:** {pdf.name} | **Size:** {pdf.size:,} bytes")

# Chat interface
if knowledgeBase:
    st.markdown("---")
    st.markdown("### 💬 Chat with your document")
    
    # Display chat history
    chat_container = st.container()
    with chat_container:
        for i, (question, answer) in enumerate(st.session_state.chat_history):
            st.markdown(f'''
            <div class="user-message">
                <strong>You:</strong> {question}
            </div>
            ''', unsafe_allow_html=True)
            
            st.markdown(f'''
            <div class="bot-message">
                <strong>AI Assistant:</strong> {answer}
            </div>
            ''', unsafe_allow_html=True)
    
    # Chat input
    col1, col2 = st.columns([4, 1])
    
    with col1:
        question = st.text_input(
            "Ask a question or request a summary...",
            placeholder="e.g., 'What is the main topic of this document?' or 'Give me a summary'",
            label_visibility="collapsed",
            key="chat_input"
        )
    
    with col2:
        send_button = st.button("Send 🚀", use_container_width=True)
    
    # Process question
    if send_button and question.strip():
        with st.spinner("🤔 Thinking..."):
            answer = ask_pdf_question(knowledgeBase, question)
        
        st.session_state.chat_history.append((question, answer))
        st.rerun()
    
    # Suggested questions
    if not st.session_state.chat_history:
        st.markdown("### 💡 Try these sample questions:")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📋 Summarize this document", use_container_width=True):
                st.session_state.chat_input = "Please provide a comprehensive summary of this document"
                st.rerun()
        
        with col2:
            if st.button("🎯 What are the key points?", use_container_width=True):
                st.session_state.chat_input = "What are the main key points discussed in this document?"
                st.rerun()
        
        with col3:
            if st.button("🔍 Find important details", use_container_width=True):
                st.session_state.chat_input = "What are the most important details I should know from this document?"
                st.rerun()

else:
    st.markdown("""
    <div style="text-align: center; padding: 3rem; color: #7f8c8d;">
        <h3>📁 No document uploaded yet</h3>
        <p>Upload a PDF document above to start your intelligent conversation!</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: rgba(0,0,0,0.6); padding: 1rem;">
    <p>Built with ❤️ using Streamlit & Hugging Face | Powered by AI</p>
</div>
""", unsafe_allow_html=True)