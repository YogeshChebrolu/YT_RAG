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