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
            # Enhanced prompt for better structured summaries
            prompt = f"""
Analyze and summarize this article with a professional, well-structured format. Provide:

1. **Main Topic/Title**: A clear, concise title describing what the article is about
2. **Key Points**: Break down the main ideas into bullet points with clear explanations
3. **Important Details**: Include specific facts, numbers, or notable mentions
4. **Summary**: A brief concluding paragraph tying everything together

Format your response with clear headings, bullet points, and organized structure. Make it informative and easy to scan.

Article content:
{text[:6000]}
"""
            
            response = openai_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system", 
                        "content": "You are an expert content analyst. Provide well-structured, professional summaries with clear formatting using markdown. Focus on extracting key insights and organizing information in an easy-to-read format."
                    },
                    {
                        "role": "user", 
                        "content": prompt
                    }
                ],
                temperature=0.3,  # Lower temperature for more consistent, factual summaries
                max_tokens=1000   # Allow for longer, more detailed summaries
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
    
    return f"""📄 **Article Extract:**

{summary}

💡 *For AI-powered structured summaries with key points and analysis, configure OpenAI API key in Streamlit secrets.*"""
