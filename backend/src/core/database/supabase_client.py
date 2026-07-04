from dotenv import load_dotenv
import os
from supabase import create_client, Client
load_dotenv()

def get_supabase_client():
  url: str = os.environ.get("SUPABASE_URL")
  key: str = os.environ.get("SUPABASE_KEY")
  supabase: Client = create_client(url, key)
  return supabase


""" response = (
    supabase.table("processed_videos")
    .select("*")
    .execute()
)
print(response) """