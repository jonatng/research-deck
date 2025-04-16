from supabase import create_client
import os

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def store_summary(url: str, summary: str):
    data = {"url": url, "summary": summary}
    response = supabase.table("summaries").insert(data).execute()
    return response