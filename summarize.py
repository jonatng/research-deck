import os
from llm_clients import openai_client

def summarize_text(text, method=None):
    # Auto-detect method if not provided
    if method is None:
        if openai_client:
            method = "openai"
        else:
            method = "basic"

    # OpenAI path
    if method == "openai" and openai_client:
        try:
            prompt = f"Summarize the main points of this article in a clear, concise manner:\n\n{text[:5000]}"
            response = openai_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}]
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"❌ OpenAI error: {e}")
            return create_basic_summary(text)

    # Basic text extraction (no AI)
    elif method == "basic":
        return create_basic_summary(text)

    # Fallback if method is invalid
    else:
        return create_basic_summary(text)

def create_basic_summary(text):
    """Create a basic summary when AI models are not available"""
    # Take first few sentences as a basic summary
    sentences = text.split('. ')
    summary_sentences = sentences[:5]  # Take first 5 sentences
    summary = '. '.join(summary_sentences)
    if not summary.endswith('.'):
        summary += '.'
    
    # Limit length
    if len(summary) > 1000:
        summary = summary[:1000] + "..."
    
    return f"📄 **Article Extract:**\n\n{summary}\n\n💡 *For AI-powered summaries, configure OpenAI API key in Space settings.*"
