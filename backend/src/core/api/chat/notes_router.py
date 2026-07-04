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
from core.api.chat.create_notes import match_notes_headings,update_notes_status
from core.api.chat.models import Update_Notes_Status_Response,Update_Notes_Status_Request


notes_router = APIRouter()

@notes_router.post("/create_notes", response_model=CreateNotesResponse)
async def create_notes_route(
    request: CreateNotesRequest,
    user: Dict[str, Any] = Depends(verify_current_user),
    supabase: AsyncClient = Depends(get_supabase_client)
):
    try:
        response = create_notes(user_id=user.id, video_id=request.video_id, instruction=request.query)
        content, notes_id = response
        return CreateNotesResponse(
            content=content,
            notes_id=notes_id
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create notes: {e}")



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
from core.api.chat.create_notes import match_notes_headings,update_notes_status
from core.api.chat.models import Update_Notes_Status_Response,Update_Notes_Status_Request


notes_router = APIRouter()

@notes_router.post("/create_notes", response_model=CreateNotesResponse)
async def create_notes_route(
    request: CreateNotesRequest,
    user: Dict[str, Any] = Depends(verify_current_user),
    supabase: AsyncClient = Depends(get_supabase_client)
):
    try:
        response = create_notes(user_id=user.id, video_id=request.video_id, instruction=request.query)
        content, notes_id = response
        return CreateNotesResponse(
            content=content,
            notes_id=notes_id
        )
    except Exception as e:
        # Return a clear error message to the client
        raise HTTPException(status_code=500, detail=f"Failed to create notes: {e}")



@notes_router.get("/match_notes_headings", response_model=list[Match_Notes_HeadingsResponse])
async def match_notes(
    query: str,
    user: Dict[str, Any] = Depends(verify_current_user),
    supabase: AsyncClient = Depends(get_supabase_client)
):
    try:
        data = match_notes_headings(user_id=user.id, query=query)
        if data is False or data is None:
            raise HTTPException(status_code=500, detail="Failed to match notes headings")
        results = [Match_Notes_HeadingsResponse(**item) for item in data]
        return results
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to match notes headings: {e}")
    


@notes_router.post("/update_notes_status",response_model=Update_Notes_Status_Response)
async def update_notes(
    request: Update_Notes_Status_Request,
    user: Dict[str, Any] = Depends(verify_current_user),
    supabase: AsyncClient = Depends(get_supabase_client)
):
    response=update_notes_status(notes_id=request.notes_id,status=request.status)
    return Update_Notes_Status_Response(
        response=response
    )
