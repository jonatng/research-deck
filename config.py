import os
from dotenv import load_dotenv
load_dotenv()  # Load .env file for local dev

REQUIRED_ENV_VARS = [
    # No required vars - make everything optional for flexible deployment
]

OPTIONAL_ENV_VARS = [
    "SUPABASE_URL",
    "SUPABASE_KEY",
    "OPENAI_API_KEY",
    "USE_OPENAI",
]

def validate_env():
    missing = [var for var in REQUIRED_ENV_VARS if not os.getenv(var)]
    if missing:
        print(f"⚠️ Warning: Missing environment variables: {', '.join(missing)}")
        print("Some features may not work properly.")
        # Don't raise an error, just warn
        return False
    return True