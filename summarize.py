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
            # Provide a basic fallback summary
            return create_fallback_summary(text)

    # OpenAI path
    if method == "openai" and openai_client:
        try:
            response = openai_client.chat.completions.create(
                model="gpt-4o-mini",  # Updated to correct model name
                messages=[{"role": "user", "content": prompt}]
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"❌ OpenAI error: {e}")
            return create_fallback_summary(text)

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
            return create_fallback_summary(text)

    # Fallback if method is invalid
    else:
        return create_fallback_summary(text)

def create_fallback_summary(text):
    """Create a basic summary when AI models are not available"""
    # Take first few sentences as a basic summary
    sentences = text.split('. ')
    summary_sentences = sentences[:3]  # Take first 3 sentences
    summary = '. '.join(summary_sentences)
    if not summary.endswith('.'):
        summary += '.'
    
    return f"📄 Basic Summary (AI models unavailable):\n\n{summary}\n\n⚠️ This is a basic text excerpt. For AI-powered summaries, please configure OpenAI API key."
