import os
from dotenv import load_dotenv
load_dotenv()  # Load .env file for local dev

# Check if running on Hugging Face Spaces
IS_HUGGINGFACE_SPACE = os.getenv("SPACE_ID") is not None

REQUIRED_ENV_VARS = [
    # No required vars for HF Spaces - make everything optional
]

OPTIONAL_ENV_VARS = [
    "SUPABASE_URL",
    "SUPABASE_KEY",
    "HUGGINGFACE_TOKEN",
    "OPENAI_API_KEY",
    "USE_OPENAI",
]

def validate_env():
    if IS_HUGGINGFACE_SPACE:
        print("🚀 Running on Hugging Face Spaces - using minimal configuration")
        return True
        
    missing = [var for var in REQUIRED_ENV_VARS if not os.getenv(var)]
    if missing:
        print(f"⚠️ Warning: Missing environment variables: {', '.join(missing)}")
        print("Some features may not work properly.")
        # Don't raise an error, just warn
        return False
    return True