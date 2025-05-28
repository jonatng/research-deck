from dotenv import load_dotenv
load_dotenv()

# Import but don't initialize immediately to avoid blocking
from llm_clients import initialize_clients, openai_client

import os
import json
import streamlit as st
import tempfile
from datetime import datetime

from article_info_extractor import get_article_content
from ppt_handler import create_ppt_with_summaries, append_to_existing_ppt
from db import insert_summary
from summarize import summarize_text
from config import validate_env
from login_page import require_login, show_user_header
from auth import get_current_user, create_test_user

# === Validate Environment Variables ===
validate_env()

# === Initialize Test User ===
# Create test user on startup if database is available
try:
    create_test_user()
except Exception as e:
    print(f"⚠️ Could not create test user: {e}")

# === Streamlit UI Setup ===
st.set_page_config(
    page_title="AI Research Deck",
    page_icon="📰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# === Authentication Check ===
require_login()

# === Initialize Session State ===
def init_session_state():
    """Initialize session state variables"""
    if 'processing' not in st.session_state:
        st.session_state.processing = False
    if 'summaries' not in st.session_state:
        st.session_state.summaries = {}
    if 'last_processed_urls' not in st.session_state:
        st.session_state.last_processed_urls = []
    if 'show_debug' not in st.session_state:
        st.session_state.show_debug = False
    if 'max_urls' not in st.session_state:
        st.session_state.max_urls = 5

# Initialize session state
init_session_state()

# === Custom CSS for Beautiful Styling ===
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    
    .feature-card {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #667eea;
        margin: 1rem 0;
    }
    
    .status-card {
        background: #e8f5e8;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #4caf50;
        margin: 0.5rem 0;
    }
    
    .warning-card {
        background: #fff3cd;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #ffc107;
        margin: 0.5rem 0;
    }
    
    .stButton > button {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.75rem 2rem;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
    }
    
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# === Header Section ===
current_user = get_current_user()
st.markdown(f"""
<div class="main-header">
    <h1>📰 AI Research Deck</h1>
    <p style="font-size: 1.2rem; margin: 0;">Welcome back, {current_user['username']}! Transform articles into insights with AI-powered summarization</p>
</div>
""", unsafe_allow_html=True)

# === Initialize LLM Clients ===
# Initialize clients when needed, not at import time
if 'clients_initialized' not in st.session_state:
    try:
        initialize_clients()
        st.session_state.clients_initialized = True
    except Exception as e:
        st.session_state.clients_initialized = False
        st.session_state.client_error = str(e)

# === Sidebar Configuration ===
with st.sidebar:
    st.header("⚙️ Configuration")
    
    # Model Selection with better UI
    st.subheader("🤖 AI Model Selection")
    
    model_choice = st.selectbox(
        "Choose your AI engine:",
        ["OpenAI GPT (API Key Required)", "Basic Text Extraction (No AI)"],
        help="OpenAI provides high-quality AI summaries, or use basic text extraction",
        key="model_choice"
    )
    
    # Status indicators
    st.subheader("📊 System Status")
    
    # Show client initialization status
    if not st.session_state.get('clients_initialized', False):
        if 'client_error' in st.session_state:
            st.warning(f"⚠️ Client initialization issue: {st.session_state.client_error}")
    
    if openai_client:
        st.success("✅ OpenAI: Available")
    else:
        st.warning("⚠️ OpenAI: Not configured")
    
    # Advanced Options
    with st.expander("🔧 Advanced Options"):
        st.session_state.show_debug = st.checkbox(
            "Show debug information", 
            value=st.session_state.show_debug,
            key="debug_checkbox"
        )
        st.session_state.max_urls = st.slider(
            "Max URLs to process", 
            1, 10, 
            value=st.session_state.max_urls,
            key="max_urls_slider"
        )
        
    # Help Section
    with st.expander("❓ How to Use"):
        st.markdown("""
        **💻 Usage Instructions:**
        1. **Enter URLs**: Paste article URLs (one per line)
        2. **Choose Mode**: Select OpenAI GPT or Basic Extraction
        3. **Optional**: Upload existing PowerPoint to append to
        4. **Run**: Click the processing button
        5. **Download**: Get your PowerPoint presentation
        
        💡 **Tip**: Configure OPENAI_API_KEY in Streamlit secrets for AI summaries
        """)

# === Main Content Area ===
col1, col2 = st.columns([2, 1])

with col1:
    st.header("📝 Article Input")
    
    # URL Input with better styling
    urls_input = st.text_area(
        "Enter website URLs (one per line):",
        height=150,
        placeholder="https://example.com/article1\nhttps://example.com/article2\n...",
        help="Paste the URLs of articles you want to summarize",
        key="urls_input"
    )
    
    urls = [url.strip() for url in urls_input.splitlines() if url.strip()]
    
    if urls:
        st.success(f"📊 {len(urls)} URL(s) ready for processing")
        if len(urls) > st.session_state.max_urls:
            st.warning(f"⚠️ Only the first {st.session_state.max_urls} URLs will be processed")
            urls = urls[:st.session_state.max_urls]

with col2:
    st.header("📎 PowerPoint Options")
    
    # File upload with better styling
    uploaded_pptx = st.file_uploader(
        "Upload existing PowerPoint (optional):",
        type=["pptx"],
        help="Upload a PowerPoint file to append summaries to existing slides",
        key="pptx_uploader"
    )
    
    if uploaded_pptx:
        st.success("✅ PowerPoint file uploaded")
        st.info(f"📄 File: {uploaded_pptx.name}")

# === Method Selection Logic ===
if openai_client and ("OpenAI" in model_choice or model_choice == "OpenAI GPT"):
    selected_method = "openai"
    st.info("🚀 Using OpenAI GPT - High quality AI summaries!")
elif "Basic Text Extraction" in model_choice:
    selected_method = "basic"
    st.info("📄 Using basic text extraction - No AI processing")
else:
    selected_method = None
    st.error("❌ OpenAI API key not configured. Please set OPENAI_API_KEY in Streamlit secrets or use Basic mode.")
    st.info("💡 Go to Streamlit app settings → Secrets → Add OPENAI_API_KEY")
    st.info("🔄 Or use 'Basic Text Extraction' mode for simple article extraction")

# === Processing Functions ===
def process_urls(urls, method):
    summaries = {}
    progress_bar = st.progress(0)
    status_text = st.empty()
    current_user = get_current_user()
    user_id = current_user['id'] if current_user else None
    
    for i, url in enumerate(urls):
        progress = (i + 1) / len(urls)
        progress_bar.progress(progress)
        status_text.text(f"Processing {i+1}/{len(urls)}: {url[:50]}...")
        
        try:
            with st.spinner(f"🔍 Extracting content from: {url}"):
                article = get_article_content(url)

                combined_text = "\n".join(filter(None, [
                    article.get("text"),
                    article.get("meta_description"),
                    json.dumps(article.get("open_graph"), indent=2)
                ]))

                if not combined_text.strip():
                    st.error(f"⚠️ No extractable content found for {url}")
                    continue

                summary = summarize_text(combined_text, method=method)
                summaries[url] = summary
                # Associate summary with current user
                insert_summary(url, summary, user_id)
                
                if st.session_state.show_debug:
                    with st.expander(f"Debug: {url}"):
                        st.text(f"Content length: {len(combined_text)} characters")
                        st.text(f"Summary length: {len(summary)} characters")

        except Exception as e:
            error_msg = str(e).lower()
            if any(term in error_msg for term in ["429", "too many requests", "rate limit", "quota exceeded", "insufficient_quota"]):
                st.error("🚫 API rate limit exceeded. Please try again later or use Basic Text Extraction mode.")
                if method == "openai":
                    break
            else:
                st.error(f"❌ Error processing {url}: {str(e)}")

    progress_bar.progress(1.0)
    status_text.text("✅ Processing complete!")
    return summaries

def export_to_powerpoint(summaries, uploaded_file=None):
    with st.spinner("📊 Creating PowerPoint presentation..."):
        if uploaded_file:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pptx") as tmp:
                tmp.write(uploaded_file.read())
                tmp_path = tmp.name
            append_to_existing_ppt(tmp_path, summaries)
            
            col1, col2 = st.columns(2)
            with col1:
                st.success("✅ Summaries appended to your PowerPoint!")
            with col2:
                with open("appended.pptx", "rb") as f:
                    st.download_button(
                        "📥 Download Updated PowerPoint",
                        f,
                        file_name=f"updated_summaries_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pptx",
                        mime="application/vnd.openxmlformats-officedocument.presentationml.presentation",
                        key="download_updated_pptx"
                    )
        else:
            create_ppt_with_summaries(summaries)
            
            col1, col2 = st.columns(2)
            with col1:
                st.success("✅ New PowerPoint presentation created!")
            with col2:
                with open("summaries.pptx", "rb") as f:
                    st.download_button(
                        "📥 Download PowerPoint",
                        f,
                        file_name=f"summaries_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pptx",
                        mime="application/vnd.openxmlformats-officedocument.presentationml.presentation",
                        key="download_new_pptx"
                    )

# === Main Action Button ===
st.markdown("---")

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    # Disable button during processing
    button_disabled = st.session_state.processing or not urls or not selected_method
    
    if st.button(
        "🚀 Start Summarization", 
        use_container_width=True, 
        disabled=button_disabled,
        key="start_button"
    ):
        if not urls:
            st.warning("⚠️ Please enter at least one URL to get started.")
        elif not selected_method:
            st.error("❌ Please configure an AI model to proceed.")
        else:
            st.session_state.processing = True
            st.balloons()
            
            try:
                summaries = process_urls(urls, selected_method)
                if summaries:
                    st.session_state.summaries = summaries
                    st.session_state.last_processed_urls = urls
                    export_to_powerpoint(summaries, uploaded_pptx)
                    st.success("🎉 All done! Your research deck is ready!")
                    
                    # Show summary statistics
                    st.subheader("📈 Summary Statistics")
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("URLs Processed", len(summaries))
                    with col2:
                        total_chars = sum(len(summary) for summary in summaries.values())
                        st.metric("Total Summary Length", f"{total_chars:,} chars")
                    with col3:
                        method_name = "OpenAI GPT" if selected_method == "openai" else "Basic Extraction"
                        st.metric("Processing Method", method_name)
            finally:
                st.session_state.processing = False

# === Show Processing Status ===
if st.session_state.processing:
    st.info("🔄 Processing in progress... Please wait.")

# === Footer Section ===
st.markdown("---")

# Support and Social Links
col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    ### 💝 Support This Project
    Help keep this tool free and improve its features!
    
    [![Venmo](https://img.shields.io/badge/Venmo-@jonatng-blue?style=for-the-badge&logo=venmo)](https://venmo.com/u/jonatng)
    """)

with col2:
    st.markdown("""
    ### 🤝 Connect & Follow
    Stay updated with the latest features and improvements!
    
    [![LinkedIn](https://img.shields.io/badge/LinkedIn-jonatng-blue?style=for-the-badge&logo=linkedin)](https://www.linkedin.com/in/jonatng/)
    """)

# Model Information
with st.expander("ℹ️ About Processing Options"):
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **🚀 OpenAI GPT**
        - ✅ High-quality AI summaries
        - ✅ Fast processing
        - ✅ Advanced understanding
        - ⚠️ Requires API key
        - ⚠️ Usage costs apply
        """)
    
    with col2:
        st.markdown("""
        **📄 Basic Text Extraction**
        - ✅ Free to use
        - ✅ No API keys required
        - ✅ Works immediately
        - ⚠️ No AI processing
        - ⚠️ Simple text excerpts only
        """)

# Version and Credits
st.markdown("""
<div style="text-align: center; color: #666; margin-top: 2rem;">
    <small>AI Research Deck v2.1 | Built with ❤️ using Streamlit & OpenAI | Optimized for Streamlit Cloud</small>
</div>
""", unsafe_allow_html=True)
