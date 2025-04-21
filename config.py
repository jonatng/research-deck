import os
from dotenv import load_dotenv
load_dotenv()  # Load .env file for local dev

REQUIRED_ENV_VARS = [
    "SUPABASE_URL",
    "SUPABASE_KEY",
    "HUGGINGFACE_TOKEN",  # Add more if needed
]

def validate_env():
    missing = [var for var in REQUIRED_ENV_VARS if not os.getenv(var)]
    if missing:
        raise EnvironmentError(
            f"🚨 Missing required environment variables: {', '.join(missing)}"
        )