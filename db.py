import os
from supabase import create_client, Client
from datetime import datetime

# Check if running on Hugging Face Spaces
IS_HUGGINGFACE_SPACE = os.getenv("SPACE_ID") is not None

# Supabase configuration
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Initialize Supabase client only if credentials are available
supabase: Client = None
if SUPABASE_URL and SUPABASE_KEY:
    try:
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
        print("✅ Supabase client initialized successfully")
    except Exception as e:
        print(f"⚠️ Supabase initialization failed: {e}")
        supabase = None
else:
    if IS_HUGGINGFACE_SPACE:
        print("🚀 Running on Hugging Face Spaces - Database features disabled")
    else:
        print("⚠️ Supabase credentials not found - database features disabled")

def insert_summary(url: str, summary: str) -> bool:
    """Insert a summary into the database. Returns True if successful, False otherwise."""
    if not supabase:
        print("⚠️ Database not available - skipping summary storage")
        return False
        
    try:
        data = {
            "url": url,
            "summary": summary,
            "created_at": datetime.now().isoformat()
        }
        
        result = supabase.table("summaries").insert(data).execute()
        print(f"✅ Summary stored in database for {url}")
        return True
        
    except Exception as e:
        print(f"❌ Failed to store summary in database: {e}")
        return False

def get_summaries():
    """Retrieve all summaries from the database."""
    if not supabase:
        print("⚠️ Database not available")
        return []
        
    try:
        result = supabase.table("summaries").select("*").execute()
        return result.data
    except Exception as e:
        print(f"❌ Failed to retrieve summaries: {e}")
        return []
