from fastapi import APIRouter, Depends, HTTPException, status
from typing import Dict
from supabase import AsyncClient

from core.lib.db import get_supabase_client
from core.lib.auth import verify_current_user
from yt_rag.processors import process_youtube_video

video_router = APIRouter()

@video_router.post("/{video_id}/process_video")
async def process_video(
    video_id: str,
    user: Dict[str, any] = Depends(verify_current_user),
    supabase: AsyncClient = Depends(get_supabase_client)
):
    try:
        response = (
            await supabase.table("videos")
            .select("video_id")
            .eq("video_id", video_id)
            .execute()
        )
        if len(response.data) > 0:
            return {"status": "processed"}
        
        youtube_url = f"https://youtube.com/watch?v={video_id}"
        response = await process_youtube_video(youtube_url)
        
        if response:
            return {"status": "processed"}
        else:
            return {"status": "failed"}
    except:
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process video: {video_id}"
        )

@video_router.get("/{video_id}/video_status")
async def get_video_status(
    video_id: str,
    supabase: AsyncClient = Depends(get_supabase_client)
):
    try:
        status_response = await supabase.table("videos").select("processed").eq("video_id",video_id).execute()
        if status_response and len(status_response.data) > 0:
            if status_response.data[0]["processed"] == "SUCCESS":
                return {"status": "processed"}
            elif status_response.data[0]["processed"] == "PROCESSING":
                return {"status": "processing"}
            else:
                return {"status": "not_processed"}
        else:
            return {"status": "not_processed"}
    except Exception as e:
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch video status"
        )
        