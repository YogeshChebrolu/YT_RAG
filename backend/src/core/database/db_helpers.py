from core.database.supabase_client import get_supabase_client
import os
import uuid
import base64
from datetime import datetime
from typing import Optional, Dict, Any

def video_exists(video_id: str) -> bool:
    supabase = get_supabase_client()
    response = (
        supabase.table("videos")
        .select("id")
        .eq("video_id", video_id)
        .limit(1)
        .execute()
    )
    return len(response.data) > 0


def push_video_details(id,video_id,summary_text):
  """
  video_id text primary key not null,
  created_at timestamp with time zone not null default now(),
  title text,
  summary text,
  channel_name text,
  processed public.video_status
  """
  supabase=get_supabase_client()
  response = (
    supabase.table("videos")
    .insert({"video_id": video_id,"summary":summary_text})
    .execute()
  )
  return response


def list_folder_contents_os_walk(start_path):
    total_files=[]
    for root, dirs, files in os.walk(start_path):
        if dirs:
          for dir in dirs:
            for file in files:
              file_path=root+"/"+dir+"/"+file
              total_files.append(file_path)
        else:
          for file in files:
            file_path=root+"/"+file
            total_files.append(file_path)
           
    return total_files


def match_notes_headings(user_id,query_embedding):
    try:
      query_embedding=query_embedding.tolist() if isinstance(query_embedding, np.ndarray) else query_embedding
      print("Matching notes with headings")
      res = client.rpc(
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


# Screenshot and Watchtime Helper Functions
def store_user_screenshot(
    user_id: str,
    video_id: str,
    screenshot_data_url: str,
    timestamp_seconds: float,
    description: Optional[str] = None
) -> Dict[str, Any]:
    """
    Store a user-captured screenshot with timestamp metadata in Supabase.
    The screenshot is stored in the Supabase storage bucket and metadata in user_screenshots table.
    """
    supabase = get_supabase_client()

    try:
        # Extract base64 data from data URL
        # Format: data:image/jpeg;base64,/9j/4AAQSkZJRg...
        if "base64," in screenshot_data_url:
            base64_data = screenshot_data_url.split("base64,")[1]
        else:
            base64_data = screenshot_data_url

        # Decode base64 to bytes
        image_bytes = base64.b64decode(base64_data)

        # Generate unique filename
        screenshot_id = str(uuid.uuid4())
        file_path = f"user_screenshots/{user_id}/{video_id}/{screenshot_id}.jpg"

        # Upload to Supabase storage
        supabase.storage.from_("video-frames").upload(
            path=file_path,
            file=image_bytes,
            file_options={"content-type": "image/jpeg"}
        )

        # Get public URL
        screenshot_url = supabase.storage.from_("video-frames").get_public_url(file_path)

        # Store metadata in database
        response = supabase.table("user_screenshots").insert({
            "id": screenshot_id,
            "user_id": user_id,
            "video_id": video_id,
            "screenshot_url": screenshot_url,
            "timestamp_seconds": timestamp_seconds,
            "description": description,
            "created_at": datetime.utcnow().isoformat()
        }).execute()

        return {
            "screenshot_id": screenshot_id,
            "screenshot_url": screenshot_url,
            "timestamp_seconds": timestamp_seconds
        }

    except Exception as e:
        print(f"Error storing screenshot: {e}")
        return None


def update_user_watchtime(
    user_id: str,
    video_id: str,
    current_position_seconds: float,
    total_watched_seconds: Optional[float] = None
) -> Dict[str, Any]:
    """
    Update or create user watchtime record for a video.
    Tracks current position and total watched time.
    """
    supabase = get_supabase_client()

    try:
        # Check if record exists
        existing = supabase.table("user_watchtime").select("*").eq(
            "user_id", user_id
        ).eq("video_id", video_id).execute()

        if len(existing.data) > 0:
            # Update existing record
            record = existing.data[0]
            updated_total = total_watched_seconds if total_watched_seconds else record.get("total_watched_seconds", 0)

            response = supabase.table("user_watchtime").update({
                "current_position_seconds": current_position_seconds,
                "total_watched_seconds": updated_total,
                "last_watched_at": datetime.utcnow().isoformat()
            }).eq("id", record["id"]).execute()
        else:
            # Create new record
            response = supabase.table("user_watchtime").insert({
                "user_id": user_id,
                "video_id": video_id,
                "current_position_seconds": current_position_seconds,
                "total_watched_seconds": total_watched_seconds or 0,
                "last_watched_at": datetime.utcnow().isoformat()
            }).execute()

        return response.data[0] if response.data else None

    except Exception as e:
        print(f"Error updating watchtime: {e}")
        return None


def get_user_watchtime(user_id: str, video_id: str) -> Optional[Dict[str, Any]]:
    """
    Retrieve user's watchtime data for a specific video.
    """
    supabase = get_supabase_client()

    try:
        response = supabase.table("user_watchtime").select("*").eq(
            "user_id", user_id
        ).eq("video_id", video_id).execute()

        return response.data[0] if response.data else None

    except Exception as e:
        print(f"Error fetching watchtime: {e}")
        return None


def get_user_screenshots(
    user_id: str,
    video_id: str,
    timestamp_range: Optional[tuple] = None
) -> list:
    """
    Get all user screenshots for a video, optionally filtered by timestamp range.

    Args:
        user_id: User ID
        video_id: Video ID
        timestamp_range: Optional tuple of (start_seconds, end_seconds)
    """
    supabase = get_supabase_client()

    try:
        query = supabase.table("user_screenshots").select("*").eq(
            "user_id", user_id
        ).eq("video_id", video_id)

        if timestamp_range:
            start, end = timestamp_range
            query = query.gte("timestamp_seconds", start).lte("timestamp_seconds", end)

        response = query.order("timestamp_seconds").execute()

        return response.data

    except Exception as e:
        print(f"Error fetching screenshots: {e}")
        return []