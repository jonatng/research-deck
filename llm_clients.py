# llm_clients.py

import os

openai_client = None

# Check if running on Hugging Face Spaces
IS_HUGGINGFACE_SPACE = os.getenv("SPACE_ID") is not None

def initialize_clients():
    global openai_client

    # Try to initialize OpenAI client if API key is available
    if os.getenv("OPENAI_API_KEY"):
        try:
            from openai import OpenAI
            openai_client = OpenAI()
            print("✅ OpenAI client initialized successfully")
        except ImportError:
            print("⚠️ OpenAI package not available - AI features disabled")
            openai_client = None
        except Exception as e:
            print(f"⚠️ OpenAI client initialization failed: {e}")
            openai_client = None
    else:
        if IS_HUGGINGFACE_SPACE:
            print("🚀 Running on Hugging Face Spaces - Set OPENAI_API_KEY in Space settings for AI features")
        else:
            print("⚠️ OPENAI_API_KEY not found - AI features disabled")
        openai_client = None
