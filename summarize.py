import os
from llm_clients import openai_client, ollama_client, OLLAMA_MODEL

def summarize_text(text, method=None):
    prompt = f"Summarize the main points of this article:\n\n{text[:5000]}"

    # Auto-detect method if not provided
    if method is None:
        if openai_client:
            method = "openai"
        elif ollama_client:
            method = "ollama"
        else:
            raise RuntimeError("❌ No LLM client is available. Please check your environment settings.")

    # OpenAI path
    if method == "openai" and openai_client:
        try:
            response = openai_client.chat.completions.create(
                model="gpt-4.1-mini",  # Or "gpt-4" if unsupported
                messages=[{"role": "user", "content": prompt}]
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"❌ OpenAI error: {e}")
            return "Error using OpenAI"

    # Ollama path
    elif method == "ollama" and ollama_client:
        try:
            response = ollama_client.chat(
                model=OLLAMA_MODEL,
                messages=[{"role": "user", "content": prompt}]
            )
            return response["message"]["content"]
        except Exception as e:
            print(f"❌ Ollama error: {e}")
            return "Error using Ollama"

    # Fallback if method is invalid
    else:
        raise ValueError(f"❌ Unknown or unsupported summarization method: {method}")
