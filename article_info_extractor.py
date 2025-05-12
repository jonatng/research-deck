import time
import hashlib
from pathlib import Path
from bs4 import BeautifulSoup
import os
import requests
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError

# === Config ===
USE_OPENAI = os.getenv("USE_OPENAI", "false").lower() == "true"
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "deepseek-r1")

# Create cache directory if needed
CACHE_DIR = Path("cache")
CACHE_DIR.mkdir(exist_ok=True)

# === Import LLM Clients ===
if USE_OPENAI:
    from openai import OpenAI
    openai_client = OpenAI()

try:
    import ollama
except ImportError:
    raise ImportError("The 'ollama' Python package is required. Install it with `pip install ollama`.")

# === Load with Playwright ===
def load_with_playwright(url, retries=3, delay=3):
    for attempt in range(retries):
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                page = browser.new_page()
                page.goto(url, timeout=30000)
                time.sleep(delay)
                html = page.content()
                browser.close()
                return html
        except PlaywrightTimeoutError as e:
            print(f"❌ Playwright attempt {attempt + 1} failed: {e}")
            time.sleep(2)
    raise RuntimeError(f"Failed to load {url} after {retries} attempts.")

# === Extract Text & Metadata ===
def extract_article_content(html):
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()

    og_tags = {
        tag.get("property"): tag.get("content")
        for tag in soup.find_all("meta")
        if tag.get("property", "").startswith("og:")
    }

    meta_description = soup.find("meta", attrs={"name": "description"})
    metadata = {
        "meta_description": meta_description["content"] if meta_description else None,
        "og_tags": og_tags,
    }

    text = soup.get_text(separator="\n")
    text = "\n".join([line.strip() for line in text.splitlines() if line.strip()])

    return text, metadata

# === Main Entry Point ===
def get_article_content(url):
    print(f"🌍 Loading: {url}")
    html = load_with_playwright(url)

    print("📄 Extracting text & metadata...")
    text, metadata = extract_article_content(html)

    return {
        "text": text,
        "meta_description": metadata["meta_description"],
        "open_graph": metadata["og_tags"]
    }
