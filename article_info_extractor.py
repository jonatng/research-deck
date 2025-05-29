import time
import hashlib
import random
from pathlib import Path
from bs4 import BeautifulSoup
import os
import requests
import base64
from typing import Dict, List, Optional

# Try to import Playwright, fallback to requests if not available
try:
    from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
    PLAYWRIGHT_AVAILABLE = True
    print("✅ Playwright available for enhanced web scraping")
except ImportError:
    print("⚠️ Playwright not available - using enhanced requests fallback")
    PLAYWRIGHT_AVAILABLE = False

# Try to import OCR capabilities (optional)
try:
    import pytesseract
    from PIL import Image
    import io
    OCR_AVAILABLE = True
    print("✅ OCR capabilities available")
except ImportError:
    print("⚠️ OCR not available - using text-only extraction")
    OCR_AVAILABLE = False

# Create cache directory if needed
CACHE_DIR = Path("cache")
CACHE_DIR.mkdir(exist_ok=True)

# === Advanced User Agents and Headers ===
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15'
]

def get_random_headers():
    """Generate randomized headers to avoid detection"""
    return {
        'User-Agent': random.choice(USER_AGENTS),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Cache-Control': 'max-age=0'
    }

# === Enhanced Playwright with Stealth ===
def load_with_stealth_playwright(url, retries=3, delay=None):
    """Load URL with Playwright using stealth techniques"""
    if delay is None:
        delay = random.uniform(2, 5)  # Random delay to seem more human
        
    for attempt in range(retries):
        try:
            with sync_playwright() as p:
                # Launch browser with stealth settings
                browser = p.chromium.launch(
                    headless=True,
                    args=[
                        '--no-sandbox',
                        '--disable-blink-features=AutomationControlled',
                        '--disable-dev-shm-usage',
                        '--disable-extensions',
                        '--disable-plugins',
                        '--disable-images',  # Faster loading
                        '--disable-javascript',  # Try without JS first
                    ]
                )
                
                # Create context with realistic settings
                context = browser.new_context(
                    user_agent=random.choice(USER_AGENTS),
                    viewport={'width': 1920, 'height': 1080},
                    locale='en-US',
                    timezone_id='America/New_York'
                )
                
                page = context.new_page()
                
                # Navigate with timeout
                page.goto(url, timeout=30000, wait_until='domcontentloaded')
                
                # Random human-like delay
                time.sleep(delay)
                
                # Try to scroll to load more content
                try:
                    page.evaluate("window.scrollTo(0, document.body.scrollHeight/2)")
                    time.sleep(1)
                    page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                    time.sleep(1)
                except:
                    pass
                
                html = page.content()
                browser.close()
                return html, 'playwright_stealth'
                
        except Exception as e:
            print(f"❌ Stealth Playwright attempt {attempt + 1} failed: {e}")
            if attempt < retries - 1:
                time.sleep(random.uniform(2, 4))
                
    raise RuntimeError(f"Failed to load {url} with stealth Playwright after {retries} attempts.")

# === Enhanced Requests with Session ===
def load_with_enhanced_requests(url, retries=3):
    """Load URL with enhanced requests using sessions and random delays"""
    session = requests.Session()
    
    for attempt in range(retries):
        try:
            # Random delay between requests
            if attempt > 0:
                time.sleep(random.uniform(1, 3))
                
            headers = get_random_headers()
            response = session.get(url, headers=headers, timeout=30, allow_redirects=True)
            response.raise_for_status()
            return response.text, 'requests_enhanced'
            
        except requests.RequestException as e:
            print(f"❌ Enhanced requests attempt {attempt + 1} failed: {e}")
            if attempt < retries - 1:
                time.sleep(random.uniform(2, 4))
                
    raise RuntimeError(f"Failed to load {url} with enhanced requests after {retries} attempts.")

# === Intelligent Content Extraction ===
def extract_with_multiple_strategies(html: str, extraction_method: str) -> Dict:
    """Try multiple extraction strategies for better content recovery"""
    soup = BeautifulSoup(html, "html.parser")
    
    # Remove unwanted elements
    for tag in soup(["script", "style", "noscript", "nav", "header", "footer", "aside", "form"]):
        tag.decompose()
    
    # Strategy 1: Look for article-specific tags
    content_selectors = [
        'article',
        '[role="main"]',
        '.article-content',
        '.post-content',
        '.entry-content',
        '.content',
        'main',
        '.article-body',
        '.story-body'
    ]
    
    main_content = None
    for selector in content_selectors:
        elements = soup.select(selector)
        if elements:
            main_content = elements[0]
            break
    
    # Strategy 2: Find largest text block if no semantic tags
    if not main_content:
        text_blocks = soup.find_all(['div', 'section', 'p'])
        if text_blocks:
            main_content = max(text_blocks, key=lambda x: len(x.get_text()))
    
    # Strategy 3: Fallback to body
    if not main_content:
        main_content = soup.find('body') or soup
    
    # Extract metadata
    meta_description = soup.find("meta", attrs={"name": "description"})
    title = soup.find('title')
    
    og_tags = {}
    for tag in soup.find_all("meta"):
        if tag.get("property", "").startswith("og:"):
            og_tags[tag.get("property")] = tag.get("content")
    
    # Extract clean text
    if main_content:
        # Remove remaining unwanted elements
        for tag in main_content(["iframe", "embed", "object", "video"]):
            tag.decompose()
            
        text = main_content.get_text(separator="\n")
        text = "\n".join([line.strip() for line in text.splitlines() if line.strip() and len(line.strip()) > 10])
    else:
        text = soup.get_text(separator="\n")
        text = "\n".join([line.strip() for line in text.splitlines() if line.strip()])
    
    return {
        "text": text,
        "title": title.get_text().strip() if title else None,
        "meta_description": meta_description["content"] if meta_description else None,
        "open_graph": og_tags,
        "extraction_method": extraction_method,
        "content_length": len(text)
    }

# === OCR Fallback for Images (Optional) ===
def extract_text_from_images(html: str, url: str) -> str:
    """Extract text from images using OCR (experimental)"""
    if not OCR_AVAILABLE:
        return ""
    
    try:
        soup = BeautifulSoup(html, "html.parser")
        img_tags = soup.find_all('img')
        
        extracted_text = []
        for img in img_tags[:3]:  # Limit to first 3 images to avoid overload
            src = img.get('src') or img.get('data-src')
            if not src:
                continue
                
            # Handle relative URLs
            if src.startswith('//'):
                src = 'https:' + src
            elif src.startswith('/'):
                from urllib.parse import urljoin
                src = urljoin(url, src)
            
            try:
                response = requests.get(src, timeout=10)
                if response.status_code == 200:
                    image = Image.open(io.BytesIO(response.content))
                    text = pytesseract.image_to_string(image)
                    if text.strip():
                        extracted_text.append(text.strip())
            except:
                continue
                
        return "\n".join(extracted_text)
    except Exception as e:
        print(f"⚠️ OCR extraction failed: {e}")
        return ""

# === Advanced Requests with Cloud Optimization ===
def load_with_cloud_optimized_requests(url, retries=3):
    """Cloud-optimized requests with advanced techniques for better success rates"""
    session = requests.Session()
    
    # More aggressive session configuration
    session.mount('http://', requests.adapters.HTTPAdapter(max_retries=3))
    session.mount('https://', requests.adapters.HTTPAdapter(max_retries=3))
    
    for attempt in range(retries):
        try:
            # Random delay between requests
            if attempt > 0:
                time.sleep(random.uniform(1, 3))
            
            headers = get_random_headers()
            
            # Add additional anti-detection headers
            headers.update({
                'DNT': '1',
                'X-Forwarded-For': f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}",
                'X-Real-IP': f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}",
                'Pragma': 'no-cache'
            })
            
            # Try different approaches
            approaches = [
                # Approach 1: Standard request
                lambda: session.get(url, headers=headers, timeout=30, allow_redirects=True),
                # Approach 2: With cookies simulation
                lambda: session.get(url, headers=headers, timeout=30, allow_redirects=True, 
                                  cookies={'session_id': f'sess_{random.randint(10000,99999)}'}),
                # Approach 3: With referrer simulation
                lambda: session.get(url, headers={**headers, 'Referer': 'https://www.google.com/'}, 
                                  timeout=30, allow_redirects=True)
            ]
            
            for i, approach in enumerate(approaches):
                try:
                    response = approach()
                    response.raise_for_status()
                    
                    # Check if we got actual content (not just an error page)
                    if len(response.text) > 500 and 'blocked' not in response.text.lower():
                        return response.text, f'requests_cloud_optimized_v{i+1}'
                    elif i < len(approaches) - 1:  # Try next approach
                        continue
                    else:
                        return response.text, 'requests_cloud_optimized_fallback'
                        
                except requests.RequestException as e:
                    if i == len(approaches) - 1:  # Last approach failed
                        raise e
                    continue
            
        except requests.RequestException as e:
            print(f"❌ Cloud-optimized requests attempt {attempt + 1} failed: {e}")
            if attempt < retries - 1:
                time.sleep(random.uniform(2, 4))
                
    raise RuntimeError(f"Failed to load {url} with cloud-optimized requests after {retries} attempts.")

# === Main Hybrid Extraction (Cloud-Aware) ===
def get_article_content(url):
    """Enhanced hybrid content extraction with cloud environment awareness"""
    print(f"🌍 Loading: {url}")
    
    html = None
    extraction_method = None
    is_cloud = is_cloud_environment()
    
    if is_cloud:
        print("☁️ Cloud environment detected - using cloud-optimized extraction")
    
    # Strategy 1: Try cloud-optimized requests first in cloud environments
    if is_cloud or not PLAYWRIGHT_AVAILABLE:
        try:
            html, extraction_method = load_with_cloud_optimized_requests(url)
            print("✅ Successfully loaded with cloud-optimized requests")
        except Exception as e:
            print(f"⚠️ Cloud-optimized requests failed: {e}")
    
    # Strategy 2: Try stealth Playwright only in local environments
    if not html and not is_cloud and PLAYWRIGHT_AVAILABLE:
        try:
            html, extraction_method = load_with_stealth_playwright(url)
            print("✅ Successfully loaded with stealth Playwright")
        except Exception as e:
            print(f"⚠️ Stealth Playwright failed: {e}")
    
    # Strategy 3: Fallback to enhanced requests
    if not html:
        try:
            html, extraction_method = load_with_enhanced_requests(url)
            print("✅ Successfully loaded with enhanced requests")
        except Exception as e:
            print(f"❌ All loading methods failed: {e}")
            raise RuntimeError(f"Could not load content from {url}")
    
    print("📄 Extracting content with multiple strategies...")
    result = extract_with_multiple_strategies(html, extraction_method)
    
    # Optional: Try OCR for additional content (only in local environments)
    if not is_cloud and OCR_AVAILABLE and len(result["text"]) < 500:
        print("🔍 Attempting OCR extraction...")
        ocr_text = extract_text_from_images(html, url)
        if ocr_text:
            result["text"] += "\n\n--- OCR Extracted Content ---\n" + ocr_text
            result["extraction_method"] += "_with_ocr"
    
    print(f"✅ Extracted {len(result['text'])} characters using {result['extraction_method']}")
    return result

# Detect if running on Streamlit Cloud or similar restricted environment
def is_cloud_environment():
    """Detect if running in a cloud environment where browser automation might fail"""
    cloud_indicators = [
        os.getenv('STREAMLIT_SHARING_MODE'),  # Streamlit Cloud
        os.getenv('HEROKU_APP_NAME'),         # Heroku
        os.getenv('VERCEL'),                  # Vercel
        os.getenv('NETLIFY'),                 # Netlify
        os.getenv('AWS_LAMBDA_FUNCTION_NAME') # AWS Lambda
    ]
    return any(indicator for indicator in cloud_indicators)
