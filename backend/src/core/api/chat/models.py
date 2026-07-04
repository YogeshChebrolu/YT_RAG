from datetime import datetime
from typing import Literal, Optional, List
from pydantic import BaseModel
import uuid
from pydantic import BaseModel
from datetime import datetime
from typing import List

class ChatRequest(BaseModel):
    video_id: str
    query: str
    notes_ids: Optional[List[str]]=None
    screenshot_data_url: Optional[str] = None  # Base64 encoded screenshot
    current_watchtime: Optional[float] = None  # Current playback position in seconds
    video_duration: Optional[float] = None  # Total video duration in seconds
class ChatResponse(BaseModel):
    content: str

class ChatMessage(BaseModel):
    id: uuid.UUID
    role: Literal["USER", "ASSISTANT"]
    content: str
    timestamp: datetime
    video_id: Optional[str] = None

class ChatHistoryRequest(BaseModel):
    video_id: str

class ChatHistoryResponse(BaseModel):
    history: List[ChatMessage]

class CreateNotesRequest(BaseModel):
    video_id: str
    query: str

class CreateNotesResponse(BaseModel):
    content: str
    notes_id: str



class Match_Notes_HeadingsResponse(BaseModel):
    notes: str
    heading_text: str
    distance: float
    similarity: float
    created_at: datetime

class update_notes_status(BaseModel):
    notes_id: str
    status: str

class Match_Notes_Headings_Request(BaseModel):
    query:str


class Update_Notes_Status_Request(BaseModel):
    notes_id: str
    status: str

class Update_Notes_Status_Response(BaseModel):
    response:bool


# Watchtime and Screenshot Models
class WatchtimeUpdate(BaseModel):
    video_id: str
    current_position_seconds: float
    total_watched_seconds: Optional[float] = None

class WatchtimeResponse(BaseModel):
    video_id: str
    total_watched_seconds: float
    current_position_seconds: float
    last_watched_at: datetime
    engagement_score: Optional[float] = None

class ScreenshotUpload(BaseModel):
    video_id: str
    screenshot_data_url: str  # Base64 encoded image
    timestamp_seconds: float
    description: Optional[str] = None

class ScreenshotResponse(BaseModel):
    screenshot_id: str
    video_id: str
    screenshot_url: str
    timestamp_seconds: float
    created_at: datetime


"""create or replace function match_notes_headings(
  user_id      uuid,
  query_embedding  vector(512)
)
returns table (
  notes text,
  heading_text      text,
  distance       double precision,
  similarity     double precision,
  created_at     timestamptz
)
language sql
stable
as $$
  select
    nt.notes,
    nt.heading_text,
    (nt.heading_embed <=> query_embedding) as distance,
    1 - (nt.heading_embed <=> query_embedding)  as similarity,
    nt.created_at
  from public.notes nt
  where nt.user_id = user_id
  order by nt.heading_embed <=> query_embedding;
$$;
"""
