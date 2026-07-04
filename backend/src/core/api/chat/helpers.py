from core.database.supabase_client import get_supabase_client

def load_history(video_id,user_id):
    supabase=get_supabase_client()
    response = (
        supabase.table("chat")
        .select("chat_messages(role, content)")
        .eq("video_id", video_id)
        .eq("user_id", user_id)
        .order("created_at", desc=False, foreign_table="chat_messages")
        .execute()
    )
    history=[]
    for message in response.data[0]["chat_messages"]:
        if message["content"]:
            if message["role"] == "USER":
                history.append({
                    "role": "user",
                    "parts": [{
                        "text": message["content"]
                    }]
                })
            else:
                history.append({
                    "role": "model",
                    "parts": [{
                        "text": message["content"]
                    }]
                })
    logger.info(f"Success=> History is loaded from supabase")
    return history
import re
import re

def extract_headings(markdown_text: str) -> str:
    for level in range(1, 7):
        pattern = re.compile(f"^{level * '#'} (.*)", re.MULTILINE)
        headings = pattern.findall(markdown_text)        
        if headings:
            return "\n".join(headings)
            
    return markdown_text
