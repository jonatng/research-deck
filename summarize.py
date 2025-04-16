import requests
import os

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
API_KEY = os.getenv("OLLAMA_API_KEY")  # Optional

def summarize_text(text: str, model="mistral") -> str:
    headers = {"Authorization": f"Bearer {API_KEY}"} if API_KEY else {}
    data = {
        "model": model,
        "prompt": f"Summarize this text for an business analyst:\n\n{text}"
    }
    response = requests.post(f"{OLLAMA_URL}/api/generate", json=data, headers=headers)
    response.raise_for_status()
    return response.json()["response"]