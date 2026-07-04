import os
from supabase import AsyncClient, create_async_client
from dotenv import load_dotenv

load_dotenv()

supabase: AsyncClient = None
async def initialize_supabase():
    """Initialize supabase"""
    global supabase
    supabase = await create_async_client(
        supabase_key=os.getenv("SUPABASE_KEY"),
        supabase_url=os.getenv("SUPABASE_URL")
    )
    
    return supabase

async def get_supabase_client():
    """Return Supabase Client"""
    global supabase
    if supabase is None :
        supabase = await initialize_supabase()
    return supabase