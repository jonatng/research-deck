import time
import hashlib
from pathlib import Path
from bs4 import BeautifulSoup
import os
import requests

# Check if running on Hugging Face Spaces
IS_HUGGINGFACE_SPACE = os.getenv("SPACE_ID") is not None

# Only import Playwright if not on HF Spaces
if not IS_HUGGINGFACE_SPACE:
    try:
        from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
        PLAYWRIGHT_AVAILABLE = True
    except ImportError:
        print("⚠️ Playwright not available - using requests fallback")
        PLAYWRIGHT_AVAILABLE = False
else:
    print("🚀 Running on Hugging Face Spaces - using requests for web scraping")
    PLAYWRIGHT_AVAILABLE = False

# Create cache directory if needed
CACHE_DIR = Path("cache")
CACHE_DIR.mkdir(exist_ok=True)

# === Load with Requests (Fallback) ===
def load_with_requests(url, retries=3):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    for attempt in range(retries):
        try:
            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            print(f"❌ Requests attempt {attempt + 1} failed: {e}")
            if attempt < retries - 1:
                time.sleep(2)
    raise RuntimeError(f"Failed to load {url} after {retries} attempts.")

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
    
    # Use appropriate loading method based on environment
    if PLAYWRIGHT_AVAILABLE and not IS_HUGGINGFACE_SPACE:
        html = load_with_playwright(url)
    else:
        html = load_with_requests(url)

    print("📄 Extracting text & metadata...")
    text, metadata = extract_article_content(html)

    return {
        "text": text,
        "meta_description": metadata["meta_description"],
        "open_graph": metadata["og_tags"]
    }
