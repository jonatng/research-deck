import os

# # Only load .env when running locally
# if os.getenv("ENV", "local") == "local":
#     from dotenv import load_dotenv
#     load_dotenv()

from supabase import create_client

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_URL.startswith("https://"):
    raise ValueError(f"Invalid or missing SUPABASE_URL: {SUPABASE_URL}")
if not SUPABASE_KEY:
    raise ValueError("SUPABASE_KEY is missing")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def insert_summary(url, summary):
    try:
        data = {"url": url, "summary": summary}
        supabase.table("summaries").insert(data).execute()
    except Exception as e:
        print(f"❌ Failed to insert: {e}")
