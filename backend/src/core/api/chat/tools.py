import json
import requests
from yt_rag.vector_store.embeddings import create_text_embeddings
from yt_rag.vector_store.pg_vector_operations import PG_Vector_search

from google.genai import types
from google.genai.types import GoogleSearch, Tool

def get_relevent_multimodal_data(video_id: str, query: str):
    query_embedding = create_text_embeddings(query)
    vector_search = PG_Vector_search()
    
    frames = vector_search.match_frames(video_id, query_embedding)
    transcripts = vector_search.match_transcript(video_id, query_embedding)
    # print(frames, transcripts)
    as_messages = {
        "role": "user",
        "parts": [
            {"text": "These are the relevant multimodal (Contains youtube frames and text transcript chunks) data to user's question. Use this data to answer intelligently if helpfull"}
        ]
    }
    for frame in frames:
        data = requests.get(frame["frame_url"][1:])
        image_bytes = data.content
        as_messages["parts"].append(
            {"inline_data":{ "mime_type":"image/jpeg", "data": image_bytes }}
        )
    data = ""
    for transcript in transcripts:
        json_data = json.loads(transcript["content"])
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