import os

# # Only load .env when running locally
# if os.getenv("ENV", "local") == "local":
#     from dotenv import load_dotenv
#     load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Initialize supabase client if credentials are available
supabase = None
if SUPABASE_URL and SUPABASE_KEY and SUPABASE_URL.startswith("https://"):
    try:
        from supabase import create_client
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
        print("✅ Supabase connected successfully")
    except Exception as e:
        print(f"⚠️ Supabase connection failed: {e}")
        supabase = None
else:
    print("⚠️ Supabase credentials not configured - database features disabled")

def insert_summary(url, summary):
    if not supabase:
        print("⚠️ Database not available - summary not saved")
        return False
    
    try:
        data = {"url": url, "summary": summary}
        supabase.table("summaries").insert(data).execute()
        print("✅ Summary saved to database")
        return True
    except Exception as e:
        print(f"❌ Failed to insert: {e}")
        return False
