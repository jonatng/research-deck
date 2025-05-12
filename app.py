from dotenv import load_dotenv
load_dotenv()

from llm_clients import initialize_clients, openai_client, ollama_client, OLLAMA_MODEL, OLLAMA_BASE_URL
initialize_clients()

import os
import json
import streamlit as st
import tempfile

from article_info_extractor import get_article_content
from ppt_handler import create_ppt_with_summaries, append_to_existing_ppt
from db import insert_summary
from summarize import summarize_text
from config import validate_env

# === Validate Environment Variables ===
validate_env()

# === Streamlit UI Setup ===
st.set_page_config(page_title="AI Researcher", layout="centered")
st.title("📰 Article Summarizer with Export to PowerPoint")

# === User Input ===
urls_input = st.text_area("Enter website URLs (one per line)")
urls = [url.strip() for url in urls_input.splitlines() if url.strip()]

model_choice = st.radio(
    "Choose Summarization Engine",
    ("OpenAI GPT", "Ollama Local Model")
)

# === Safe Method Selection Based on Availability ===
if model_choice == "OpenAI GPT" and openai_client:
    selected_method = "openai"
elif model_choice == "Ollama Local Model" and ollama_client:
    selected_method = "ollama"
else:
    selected_method = None

uploaded_pptx = st.file_uploader("Upload a PowerPoint to append to (optional)", type=["pptx"])

# === Processing URLs ===
def process_urls(urls, method):
    summaries = {}

    for url in urls:
        with st.spinner(f"🔍 Processing: {url}"):
            try:
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
                insert_summary(url, summary)

            except Exception as e:
                if "429" in error_msg or "too many requests" in error_msg or "rate limit" in error_msg or "quota exceeded" in error_msg or "insufficient_quota" in error_msg:
                    st.warning("⚠️ OpenAI API usage limit exceeded. Please try again later or switch to the Ollama local model.")
                    st.error(f"API Error: {str(e)}")
                    # You might want to break the loop here to prevent more failed API calls
                    if method == "openai":
                        break
                st.error(f"❌ Error processing {url}: {str(e)}")

    return summaries

# === PowerPoint Export ===
def export_to_powerpoint(summaries, uploaded_file=None):
    if uploaded_file:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pptx") as tmp:
            tmp.write(uploaded_file.read())
            tmp_path = tmp.name
        append_to_existing_ppt(tmp_path, summaries)
        st.success("✅ Summaries appended to uploaded PowerPoint!")
        with open("appended.pptx", "rb") as f:
            st.download_button("📥 Download Updated PowerPoint", f, file_name="updated_summaries.pptx")
    else:
        create_ppt_with_summaries(summaries)
        with open("summaries.pptx", "rb") as f:
            st.download_button("📥 Download New PowerPoint", f, file_name="summaries.pptx")

# === Button Trigger ===
if st.button("Run Summarization"):
    if not urls:
        st.warning("⚠️ Please enter at least one URL.")
    elif not selected_method:
        st.error("❌ The selected summarization engine is unavailable. Check your environment settings or Docker setup.")
    else:
        summaries = process_urls(urls, selected_method)
        if summaries:
            export_to_powerpoint(summaries, uploaded_pptx)
            st.success("✅ All done!")

# === Model Notice ===
st.warning("⚠️ **Ollama Local Model Notice**\n\nThis feature is still in development. You may experience limitations or inconsistencies.")

# === Donation Section ===
st.info("🙏 **Support This Project**\n\nWe welcome contributions to keep this tool free. "
        "Your donations help cover hosting, API usage, and development costs.\n\n"
        "💳 Donate via Venmo: [@jonatng](https://venmo.com/u/jonatng)", icon="💸")

st.info("🔗 **Follow me on LinkedIn**\n\nStay connected for updates, projects, and professional insights: "
        "[linkedin.com/in/jonatng](https://www.linkedin.com/in/jonatng/)", icon="👤")
