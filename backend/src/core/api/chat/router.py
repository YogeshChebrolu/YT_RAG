from datetime import datetime
import uuid
from core.api.chat.chat_gemini import LLMClient
from core.lib.auth import verify_current_user
from fastapi import APIRouter, HTTPException, Depends
from supabase import AsyncClient
from core.api.chat.models import ChatMessage, ChatRequest, ChatResponse, ChatHistoryResponse, ChatHistoryRequest,CreateNotesRequest,CreateNotesResponse,Match_Notes_HeadingsResponse,Match_Notes_Headings_Request
from core.lib.db import get_supabase_client
from pydantic import BaseModel
from typing import Optional, Literal, List, Dict, Any
from core.api.chat.create_notes import create_notes
chat_router = APIRouter()
from core.api.chat.create_notes import match_notes_headings,update_notes_status
from core.api.chat.models import Update_Notes_Status_Response,Update_Notes_Status_Request


@chat_router.post("/generate", response_model=ChatResponse)
async def generate_chat(
    request: ChatRequest,
    user: Dict[str, Any] = Depends(verify_current_user),
    supabase: AsyncClient = Depends(get_supabase_client)
):
    # Get the chat id if exists
    chat_session_response = (
        await supabase.table("chat")
        .select("id")
        .eq("user_id", user.id)
        .eq("video_id", request.video_id)
        .execute()
    )
    
    chat_id =""
    # Create a new chat session if it is the first time the user is chatting with the video
    if len(chat_session_response.data) == 0:
        print("Chat session not exist so let's create one")
        new_chat_session = (
            await supabase.table("chat")
            .insert({
                "video_id": request.video_id,
                "user_id": user.id
            })
            .execute()
        )
        chat_id = new_chat_session.data[0]["id"]
    else:        
        chat_id = chat_session_response.data[0]["id"]
    
    # Load the LLM
    if request.notes_ids is not None:
        llm_client = LLMClient(
            video_id=request.video_id,
            user_id=user.id,
            chat_id=chat_id,
            notes_id=request.notes_ids
        )
    else:
        llm_client = LLMClient(
            video_id=request.video_id,
            user_id=user.id,
            chat_id=chat_id
        )
    
    llm_client.load_history()
    
    response = llm_client.run(
        prompt=request.query
    )
    
    # print(response)
    
    return ChatResponse(
        content= response
    )
    

    


@chat_router.post("/chat_history", response_model=ChatHistoryResponse)
async def get_user_chat_history(
    request: ChatHistoryRequest,
    user: Dict[str, Any] = Depends(verify_current_user),
    supabase: AsyncClient = Depends(get_supabase_client)
):
    # Get the chat session if available else return empty history
    chat_session_response = (
        await supabase.table("chat")
        .select("id")
        .eq("video_id", request.video_id)
        .eq("user_id", user.id)
        .execute()
    )
    # print(chat_session_response)
    
    chat_id = ""
    if len(chat_session_response.data) == 0:
        return ChatHistoryResponse(
            history=[]
        )
    else:
        chat_id = chat_session_response.data[0]["id"]
    
    chat_history_response = (
        await supabase.table("chat_messages")
        .select("id, role, content, created_at")
        .eq("chat_id", chat_id)
        .order("created_at", desc=False)
        .execute()
    )
    
    chat_history = []
    for message in chat_history_response.data:
        if message["content"]:
            chat_history.append(
                ChatMessage(
                    id=message["id"],
                    role=message["role"],
                    content=message["content"],
                    timestamp=message["created_at"],
                    video_id=request.video_id
                )
            )
    
    return ChatHistoryResponse(history=chat_history)