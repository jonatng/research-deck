# llm_clients.py

import os

openai_client = None
ollama_client = None
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "deepseek-r1")
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")


def initialize_clients():
    global openai_client, ollama_client

    use_openai = os.getenv("USE_OPENAI", "false").lower() == "true"

    if use_openai:
        try:
            from openai import OpenAI
            openai_client = OpenAI()
        except ImportError:
            raise ImportError("The 'openai' package is required. Install it with `pip install openai`.")
    else:
        try:
            import ollama
            ollama_client = ollama
        except ImportError:
            raise ImportError("The 'ollama' package is required. Install it with `pip install ollama`.")
