# Add src directory to Python path for module resolution
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from contextlib import asynccontextmanager
from typing import Any, Dict
from core.lib.auth import get_supabase_client, verify_current_user
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from supabase import AsyncClient
import uvicorn
import asyncio
from dotenv import load_dotenv
from core.api.chat.router import chat_router
from core.api.process_video.router import video_router
from core.api.chat.notes_router import notes_router
load_dotenv()

BASE_PATH = "/core/v1"


if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())


app = FastAPI(
    title="YT_RAG core api",
    description="API service for YT_RAG",
    vesrion="0.0.0",
)

origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "UPDATE", "DELETE"],
    allow_headers=["*"]
)

@app.get(f"{BASE_PATH}/health")
def health_check():
    return {"status":"ok"}


@app.get(f"{BASE_PATH}/check_auth")
async def check_supabase(
    user: Dict[str, Any] = Depends(verify_current_user),
    supabse: AsyncClient = Depends(get_supabase_client)
):
    # print(user)
    return {
        "user": user
    }
    
app.include_router(router=chat_router, prefix=f"{BASE_PATH}/chat")
app.include_router(router=video_router, prefix=f"{BASE_PATH}/video")
app.include_router(router=notes_router, prefix=f"{BASE_PATH}/notes")

def main():
    """Entry point for the application."""
    uvicorn.run(app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    main()