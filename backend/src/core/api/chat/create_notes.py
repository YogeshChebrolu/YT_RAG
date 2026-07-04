from core.database.supabase_client import get_supabase_client
from google.genai.types import Part
from yt_rag.llm_service.gemini_client import get_gemini_client
import logging
from core.assistent_prompts.prompt import notes_prompt
from yt_rag.vector_store.embeddings import create_text_embeddings
import uuid
import re
import numpy as np
logger = logging.getLogger(__name__)


def load_history(video_id, user_id):
    supabase = get_supabase_client()
    response = (
        supabase.table("chat")
        .select("chat_messages(role, content)")
        .eq("video_id", video_id)
        .eq("user_id", user_id)
        .order("created_at", desc=False, foreign_table="chat_messages")
        .execute()
    )
    history = []
    if not response.data:
        logger.info("No existing chat history found for video_id=%s user_id=%s", video_id, user_id)
        return history

    data0 = response.data[0] or {}
    chat_messages = data0.get("chat_messages") or []

    for message in chat_messages:
        if message.get("content"):
            if message.get("role") == "USER":
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
    logger.info("Success => History is loaded from supabase (%d messages)", len(history))
    return history


def extract_headings(markdown_text: str) -> str:
    for level in range(1, 7):
        pattern = re.compile(f"^{level * '#'} (.*)", re.MULTILINE)
        headings = pattern.findall(markdown_text)
        if headings:
            return "\n".join(headings)

    return markdown_text


def create_notes(user_id, video_id, instruction):
    try:
        history = load_history(video_id=video_id, user_id=user_id)
        supabase_client = get_supabase_client()
        gemini_client = get_gemini_client()
        print("Creating notes")
        history.append({
            "role": "user",
            "parts": [{
                "text": instruction
            }]
        })
        contents = history
        response = gemini_client.models.generate_content(
            model="gemini-2.0-flash",
            contents=contents,
            config={
                "system_instruction": notes_prompt,
                "temperature": 0.5,
            },
        )
        print("heading extaction")
        headings = extract_headings(markdown_text=response.text)
        print("heading extaction complete")
        print("embeddiings creation")
        embeddings = create_text_embeddings(headings)
        embeddings = embeddings.tolist() if isinstance(embeddings, np.ndarray) else embeddings
        print("embeddiings creation complete")
        print("uuid generation")
        generated_uuids = uuid.uuid4()
        generated_uuid_str = str(generated_uuids)
        print("uuid generation complete")
        print("notes insertion")

        resp = supabase_client.table("notes").insert({
            "notes_id": generated_uuid_str,
            "user_id": user_id,
            "video_id": video_id,
            "notes": response.text,
            "heading_text": headings,
            "heading_embed": embeddings,
            "notes_status": "PENDING"
        }).execute()
        print(resp)
        print("inserting complete")
        return response.text, generated_uuid_str
    except Exception as e:
        logger.exception("Failed to create notes for video_id=%s user_id=%s", video_id, user_id)
        raise


def update_notes_status(notes_id, status):
    try:
        supabase_client = get_supabase_client()
        supabase_client.table("notes").update({"notes_status": status}).eq("notes_id", notes_id).execute()
        return True
    except Exception as e:
        print(e)
        return False


def extract_notes(notes_ids):
    try:
        notes = ""
        supabase_client = get_supabase_client()
        if isinstance(notes_ids, list):
            for notes_id in notes_ids:
                response = supabase_client.table("notes").select("notes").eq("notes_id", notes_id).execute()
                if response.data:
                    notes = notes + "/n" + (response.data[0].get("notes") or "")
        else:
            response = supabase_client.table("notes").select("notes").eq("notes_id", notes_ids).execute()
            if response.data:
                notes = notes + "/n" + (response.data[0].get("notes") or "")
        return notes
    except Exception as e:
        print(e)
        return False


def match_notes_headings(user_id, query):
    try:
        supabase_client = get_supabase_client()
        query_embedding = create_text_embeddings(query)
        query_embedding = query_embedding.tolist() if isinstance(query_embedding, np.ndarray) else query_embedding
        print("Matching notes with headings")
        res = supabase_client.rpc(
            "match_notes_headings",
            {
                "user_id": user_id,
                "query_embedding": query_embedding
            }).execute()
        print("Matching notes with headings complete")
        return res.data
    except Exception as e:
        print(e)
        return False
