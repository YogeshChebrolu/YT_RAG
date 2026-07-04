from datetime import datetime
import uuid
from core.api.chat.chat_gemini import LLMClient
from core.lib.auth import verify_current_user
from fastapi import APIRouter, HTTPException, Depends
from supabase import AsyncClient
from core.api.chat.models import ChatMessage, ChatRequest, ChatResponse, ChatHistoryResponse, ChatHistoryRequest,CreateNotesRequest,CreateNotesResponse,Match_Notes_HeadingsResponse,Match_Notes_Headings_Request, WatchtimeUpdate, WatchtimeResponse, ScreenshotUpload, ScreenshotResponse
from core.lib.db import get_supabase_client
from pydantic import BaseModel
from typing import Optional, Literal, List, Dict, Any
from core.api.chat.create_notes import create_notes
chat_router = APIRouter()
from core.api.chat.create_notes import match_notes_headings,update_notes_status
from core.api.chat.models import Update_Notes_Status_Response,Update_Notes_Status_Request
from core.database.db_helpers import store_user_screenshot, update_user_watchtime, get_user_watchtime, get_user_screenshots


@chat_router.post("/generate", response_model=ChatResponse)
async def generate_chat(
    request: ChatRequest,
    user: Dict[str, Any] = Depends(verify_current_user),
    supabase: AsyncClient = Depends(get_supabase_client)
):
    # Handle screenshot upload if provided
    screenshot_context = None
    if request.screenshot_data_url and request.current_watchtime is not None:
        screenshot_result = store_user_screenshot(
            user_id=user.id,
            video_id=request.video_id,
            screenshot_data_url=request.screenshot_data_url,
            timestamp_seconds=request.current_watchtime,
            description=f"Screenshot captured at {request.current_watchtime:.2f}s"
        )
        if screenshot_result:
            screenshot_context = {
                "screenshot_id": screenshot_result["screenshot_id"],
                "screenshot_url": screenshot_result["screenshot_url"],
                "timestamp": request.current_watchtime
            }

    # Update watchtime if provided
    if request.current_watchtime is not None:
        update_user_watchtime(
            user_id=user.id,
            video_id=request.video_id,
            current_position_seconds=request.current_watchtime
        )

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

    # Get watchtime context for enhanced RAG
    watchtime_data = get_user_watchtime(user_id=user.id, video_id=request.video_id)

    # Load the LLM with additional context
    if request.notes_ids is not None:
        llm_client = LLMClient(
            video_id=request.video_id,
            user_id=user.id,
            chat_id=chat_id,
            notes_id=request.notes_ids,
            screenshot_context=screenshot_context,
            watchtime_context=watchtime_data
        )
    else:
        llm_client = LLMClient(
            video_id=request.video_id,
            user_id=user.id,
            chat_id=chat_id,
            screenshot_context=screenshot_context,
            watchtime_context=watchtime_data
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


@chat_router.post("/update_watchtime")
async def update_watchtime_endpoint(
    request: WatchtimeUpdate,
    user: Dict[str, Any] = Depends(verify_current_user)
):
    """
    Update user's watchtime for a video.
    Called by frontend to track viewing progress.
    """
    result = update_user_watchtime(
        user_id=user.id,
        video_id=request.video_id,
        current_position_seconds=request.current_position_seconds,
        total_watched_seconds=request.total_watched_seconds
    )

    if result:
        return {"status": "success", "data": result}
    else:
        raise HTTPException(status_code=500, detail="Failed to update watchtime")


@chat_router.get("/watchtime/{video_id}", response_model=WatchtimeResponse)
async def get_watchtime_endpoint(
    video_id: str,
    user: Dict[str, Any] = Depends(verify_current_user)
):
    """
    Get user's watchtime data for a specific video.
    """
    result = get_user_watchtime(user_id=user.id, video_id=video_id)

    if result:
        return WatchtimeResponse(
            video_id=result["video_id"],
            total_watched_seconds=result["total_watched_seconds"],
            current_position_seconds=result["current_position_seconds"],
            last_watched_at=result["last_watched_at"],
            engagement_score=result.get("engagement_score")
        )
    else:
        raise HTTPException(status_code=404, detail="No watchtime data found")


@chat_router.post("/upload_screenshot", response_model=ScreenshotResponse)
async def upload_screenshot_endpoint(
    request: ScreenshotUpload,
    user: Dict[str, Any] = Depends(verify_current_user)
):
    """
    Upload a user screenshot with timestamp metadata.
    """
    result = store_user_screenshot(
        user_id=user.id,
        video_id=request.video_id,
        screenshot_data_url=request.screenshot_data_url,
        timestamp_seconds=request.timestamp_seconds,
        description=request.description
    )

    if result:
        return ScreenshotResponse(
            screenshot_id=result["screenshot_id"],
            screenshot_url=result["screenshot_url"],
            timestamp_seconds=result["timestamp_seconds"],
            video_id=request.video_id,
            created_at=datetime.utcnow()
        )
    else:
        raise HTTPException(status_code=500, detail="Failed to upload screenshot")


@chat_router.get("/screenshots/{video_id}")
async def get_screenshots_endpoint(
    video_id: str,
    user: Dict[str, Any] = Depends(verify_current_user),
    start_time: Optional[float] = None,
    end_time: Optional[float] = None
):
    """
    Get all user screenshots for a video, optionally filtered by timestamp range.
    """
    timestamp_range = (start_time, end_time) if start_time and end_time else None

    screenshots = get_user_screenshots(
        user_id=user.id,
        video_id=video_id,
        timestamp_range=timestamp_range
    )

    return {"screenshots": screenshots}