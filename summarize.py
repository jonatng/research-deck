from transformers import pipeline
import os
import requests

def get_local_summarizer():
    return pipeline("summarization", model="facebook/bart-large-cnn")

def summarize_text(text, summarizer, max_len=512):
    return summarizer(text, max_length=max_len, min_length=30, do_sample=False)[0]["summary_text"]

def summarize_via_hf_api(text, model="facebook/bart-large-cnn"):
    token = os.getenv("HUGGINGFACE_TOKEN")
    if not token:
        return "[Error] Hugging Face token not found"

    headers = {"Authorization": f"Bearer {token}"}
    payload = {"inputs": text}

    response = requests.post(
        f"https://api-inference.huggingface.co/models/{model}",
        headers=headers,
        json=payload
    )

    if response.status_code == 200:
        return response.json()[0]["summary_text"]
    else:
        return f"[API Error] {response.status_code}: {response.text}"