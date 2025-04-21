from dotenv import load_dotenv
load_dotenv()
import os

import streamlit as st
import tempfile
from extractor import extract_text_from_url
from ppt_handler import create_ppt_with_summaries, append_to_existing_ppt
from db import insert_summary
from summarize import get_local_summarizer, summarize_text, summarize_via_hf_api
from config import validate_env

# Validate before anything else
validate_env()

st.set_page_config(page_title="AI Researcher", layout="centered")
st.title("📰 Website Summarizer with Export to PowerPoint")

# Input: URLs
urls_input = st.text_area("Enter website URLs (one per line)")
urls = [url.strip() for url in urls_input.splitlines() if url.strip()]

# Choose summarization method
model_choice = st.radio(
    "Choose Summarization Engine",
    ("Local Transformer", "Hugging Face API")
)

# Upload existing PowerPoint (optional)
uploaded_pptx = st.file_uploader("Upload a PowerPoint to append to (optional)", type=["pptx"])

# Trigger summarization
if st.button("Run Summarization"):
    if not urls:
        st.warning("Please enter at least one URL.")
    else:
        # Load local model only if selected
        local_summarizer = get_local_summarizer() if model_choice == "Local Transformer" else None
        summaries = {}

        for url in urls:
            with st.spinner(f"Processing: {url}"):
                text = extract_text_from_url(url)
                if not text:
                    st.error(f"Could not extract content from {url}")
                    continue

                try:
                    if model_choice == "Local Transformer":
                        summary = summarize_text(text, local_summarizer)
                    else:
                        summary = summarize_via_hf_api(text)

                    summaries[url] = summary
                    insert_summary(url, summary)

                except Exception as e:
                    st.error(f"Error summarizing {url}: {str(e)}")

        # PowerPoint export
        if uploaded_pptx:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pptx") as tmp:
                tmp.write(uploaded_pptx.read())
                tmp_path = tmp.name

            append_to_existing_ppt(tmp_path, summaries)
            st.success("✅ Summaries appended to uploaded PowerPoint!")
            with open("appended.pptx", "rb") as f:
                st.download_button("📥 Download Updated PowerPoint", f, file_name="updated_summaries.pptx")
        else:
            create_ppt_with_summaries(summaries)
            with open("summaries.pptx", "rb") as f:
                st.download_button("📥 Download New PowerPoint", f, file_name="summaries.pptx")

        st.success("✅ All done!")