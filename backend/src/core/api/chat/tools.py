import json
import requests
from yt_rag.vector_store.embeddings import create_text_embeddings
from yt_rag.vector_store.pg_vector_operations import PG_Vector_search
from core.database.db_helpers import get_user_screenshots

from google.genai import types
from google.genai.types import GoogleSearch, Tool
from typing import Optional

def get_relevent_multimodal_data(
    video_id: str,
    query: str,
    user_id: Optional[str] = None,
    screenshot_context: Optional[dict] = None,
    watchtime_context: Optional[dict] = None
):
    query_embedding = create_text_embeddings(query)
    vector_search = PG_Vector_search()

    frames = vector_search.match_frames(video_id, query_embedding)
    transcripts = vector_search.match_transcript(video_id, query_embedding)

    # Build context message
    context_parts = []

    # Add watchtime context if available
    if watchtime_context:
        current_pos = watchtime_context.get("current_position_seconds", 0)
        total_watched = watchtime_context.get("total_watched_seconds", 0)
        context_parts.append(
            f"User's watchtime context: Currently at {current_pos:.1f}s, "
            f"Total watched: {total_watched:.1f}s. "
        )

    # Add screenshot context if available
    if screenshot_context:
        context_parts.append(
            f"User captured a screenshot at {screenshot_context['timestamp']:.1f}s. "
        )

    base_text = "These are the relevant multimodal (Contains youtube frames and text transcript chunks) data to user's question. Use this data to answer intelligently if helpful."
    if context_parts:
        base_text = " ".join(context_parts) + " " + base_text

    as_messages = {
        "role": "user",
        "parts": [
            {"text": base_text}
        ]
    }

    # Add user's captured screenshot if provided
    if screenshot_context and screenshot_context.get("screenshot_url"):
        try:
            screenshot_data = requests.get(screenshot_context["screenshot_url"])
            if screenshot_data.status_code == 200:
                as_messages["parts"].append({
                    "inline_data": {
                        "mime_type": "image/jpeg",
                        "data": screenshot_data.content
                    }
                })
                as_messages["parts"].append({
                    "text": f"[User's screenshot captured at {screenshot_context['timestamp']:.1f}s]"
                })
        except Exception as e:
            print(f"Error loading user screenshot: {e}")

    # Add vector search results (existing frames)
    for frame in frames:
        data = requests.get(frame["frame_url"][1:])
        image_bytes = data.content
        as_messages["parts"].append(
            {"inline_data": {"mime_type": "image/jpeg", "data": image_bytes}}
        )

    # Add transcript data
    data = ""
    for transcript in transcripts:
        json_data = json.loads(transcript["content"])
        # Add timestamp info if available in metadata
        metadata = json_data.get("metadata", {})
        start_time = metadata.get("start_time", "")
        if start_time:
            data += f"\n[Timestamp: {start_time}s] {json_data['page_content']}"
        else:
            data += json_data["page_content"]

    as_messages["parts"].append(
        {"text": data}
    )

    return as_messages, 
        
    
    
# Prepare function declaration for the tool
rag_function_declaration = types.FunctionDeclaration(
    name="get_relevent_multimodal_data",
    description="get relevent frames and transcript chunks to users query from youtube video",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "query": types.Schema(type=types.Type.STRING, description="Efficient query for the RAG tool to find relevant data"),
        },
        required=["query"]
    ),
)

rag_tool = Tool(
    function_declarations=[rag_function_declaration]
)
web_search_tool = Tool(
    google_search=GoogleSearch()
)


def get_tools():
    return [rag_tool]

def get_tools_dict():
    return {
    "get_relevent_multimodal_data": get_relevent_multimodal_data
    }