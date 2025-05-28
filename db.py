import os
from supabase import create_client, Client
from datetime import datetime

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
    print("⚠️ Supabase credentials not found - database features disabled")

def insert_summary(url: str, summary: str, user_id: int = None) -> bool:
    """Insert a summary into the database. Returns True if successful, False otherwise."""
    if not supabase:
        print("⚠️ Database not available - skipping summary storage")
        return False
        
    try:
        data = {
            "url": url,
            "summary": summary,
            "created_at": datetime.now().isoformat(),
            "user_id": user_id  # Associate with user if provided
        }
        
        result = supabase.table("summaries").insert(data).execute()
        print(f"✅ Summary stored in database for {url}")
        return True
        
    except Exception as e:
        print(f"❌ Failed to store summary in database: {e}")
        return False

def get_summaries(user_id: int = None):
    """Retrieve summaries from the database. If user_id provided, get user-specific summaries."""
    if not supabase:
        print("⚠️ Database not available")
        return []
        
    try:
        if user_id:
            # Get user-specific summaries
            result = supabase.table("summaries").select("*").eq("user_id", user_id).execute()
        else:
            # Get all summaries (for admin or public view)
            result = supabase.table("summaries").select("*").execute()
        return result.data
    except Exception as e:
        print(f"❌ Failed to retrieve summaries: {e}")
        return []

def create_tables():
    """Create necessary tables if they don't exist"""
    if not supabase:
        print("⚠️ Database not available - cannot create tables")
        return False
    
    try:
        # Note: In Supabase, you typically create tables through the dashboard
        # This function is for reference of the expected schema
        print("📋 Expected database schema:")
        print("""
        -- Users table
        CREATE TABLE users (
            id SERIAL PRIMARY KEY,
            username VARCHAR(50) UNIQUE NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL,
            password_hash VARCHAR(255) NOT NULL,
            created_at TIMESTAMP DEFAULT NOW(),
            last_login TIMESTAMP,
            is_active BOOLEAN DEFAULT TRUE
        );
        
        -- Summaries table (updated to include user_id)
        CREATE TABLE summaries (
            id SERIAL PRIMARY KEY,
            url TEXT NOT NULL,
            summary TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT NOW(),
            user_id INTEGER REFERENCES users(id)
        );
        """)
        return True
    except Exception as e:
        print(f"❌ Error displaying schema: {e}")
        return False
