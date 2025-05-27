# llm_clients.py

import os

openai_client = None
ollama_client = None
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama2")
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

# Check if running on Hugging Face Spaces
IS_HUGGINGFACE_SPACE = os.getenv("SPACE_ID") is not None

def initialize_clients():
    global openai_client, ollama_client

    use_openai = os.getenv("USE_OPENAI", "false").lower() == "true"

    # Try to initialize OpenAI client
    if use_openai or os.getenv("OPENAI_API_KEY"):
        try:
            from openai import OpenAI
            openai_client = OpenAI()
            print("✅ OpenAI client initialized successfully")
        except ImportError:
            print("⚠️ OpenAI package not available - OpenAI features disabled")
            openai_client = None
        except Exception as e:
            print(f"⚠️ OpenAI client initialization failed: {e}")
            openai_client = None

    # Try to initialize Ollama client (skip on HF Spaces)
    if not IS_HUGGINGFACE_SPACE:
        try:
            import ollama
            ollama_client = ollama
            print("✅ Ollama client initialized successfully")
        except ImportError:
            print("⚠️ Ollama package not available - local model features disabled")
            ollama_client = None
        except Exception as e:
            print(f"⚠️ Ollama client initialization failed: {e}")
            ollama_client = None
    else:
        print("🚀 Running on Hugging Face Spaces - Ollama disabled")
        ollama_client = None
