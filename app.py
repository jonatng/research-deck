import streamlit as st
from extractor import extract_text_from_url
from summarize import summarize_text
from ppt_generator import (
    create_presentation, add_summary_slide, 
    save_presentation, append_to_existing_ppt
)
from db import store_summary

st.set_page_config(page_title="Research Deck AI", layout="centered")

st.title("🧠 AI Researcher")
url = st.text_input("Enter the article URL")

uploaded_file = st.file_uploader("Upload existing PowerPoint (optional)", type="pptx")

if st.button("Summarize"):
    with st.spinner("Processing..."):
        article = extract_text_from_url(url)
        if not article:
            st.error("Couldn't extract article.")
        else:
            summary = summarize_text(article)
            store_summary(url, summary)

            if uploaded_file:
                with open("temp_uploaded.pptx", "wb") as f:
                    f.write(uploaded_file.read())
                ppt_path = append_to_existing_ppt(summary, "temp_uploaded.pptx")
            else:
                prs = create_presentation()
                add_summary_slide(prs, summary)
                ppt_path = save_presentation(prs)

            with open(ppt_path, "rb") as f:
                st.download_button("📥 Download PowerPoint", f, file_name=os.path.basename(ppt_path))
