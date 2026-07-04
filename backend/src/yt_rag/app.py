from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel, Field, HttpUrl
from fastapi.middleware.cors import CORSMiddleware
import asyncio
import sys
from yt_rag.main import RAGPipeline

if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

app = FastAPI(
    title="RAG Pipeline API",
    description="A simple API for processing YouTube videos and chatting with conversation memory.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["chrome-extension://*"],  # Allow all Chrome extension origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

pipeline = None

class ProcessRequest(BaseModel):
    video_url: str = Field(..., description="The URL of the YouTube video to process.")

class ProcessResponse(BaseModel):
    video_id: str = Field(..., description="The ID of the processed YouTube video.")
    message: str = Field(..., description="Status message.")

class QueryRequest(BaseModel):
    query: str = Field(..., description="The question or query for the RAG pipeline.")

class QueryResponse(BaseModel):
    response: str = Field(..., description="The response from the RAG pipeline.")

class ChatRequest(BaseModel):
    prompt: str = Field(..., description="A general prompt for the chat model (no RAG).")

class ChatResponse(BaseModel):
    response: str = Field(..., description="The response from the chat model.")

class MemoryResponse(BaseModel):
    message: str = Field(..., description="Status message about the memory operation.")
    memory_size: int = Field(None, description="Current number of messages in memory, if applicable.")



@app.post("/process/", status_code=202, response_model=ProcessResponse)
async def process_video(request: ProcessRequest, background_tasks: BackgroundTasks):
    """
    Process a YouTube video and initialize the pipeline.
    """
    global pipeline
    try:
        pipeline = RAGPipeline(request.video_url)
        video_id = await pipeline.process_video()
        background_tasks.add_task(pipeline.save_conversation_memory)
        return ProcessResponse(video_id=video_id, message="Video processed successfully.")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to process video: {str(e)}")


@app.post("/query/", response_model=QueryResponse)
async def query_video(request: QueryRequest):
    """
    Query the processed video using the RAG pipeline.
    """
    global pipeline
    if not pipeline:
        raise HTTPException(status_code=400, detail="No video processed. Please call /process/ first.")
    try:
        response = pipeline.query_gemini(request.query)
        return QueryResponse(response=response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Query failed: {str(e)}")


@app.post("/chat/", response_model=ChatResponse)
async def chat_with_gemini(request: ChatRequest):
    """
    Chat with the Gemini model without RAG context, using conversation memory.
    """
    global pipeline
    if not pipeline:
        raise HTTPException(status_code=400, detail="No pipeline initialized. Please call /process/ first.")
    try:
        response = pipeline.chatgemini(request.prompt)
        return ChatResponse(response=response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chat failed: {str(e)}")


@app.post("/memory/clear/", response_model=MemoryResponse)
async def clear_memory():
    """
    Clear conversation memory.
    """
    global pipeline
    if not pipeline:
        return MemoryResponse(message="No conversation memory available.", memory_size=0)
    try:
        pipeline.clear_conversation_memory()
        return MemoryResponse(message="Conversation memory cleared.", memory_size=0)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to clear memory: {str(e)}")


@app.get("/memory/size/", response_model=MemoryResponse)
async def get_memory_size():
    """
    Get the current number of messages in conversation memory.
    """
    global pipeline
    if not pipeline:
        return MemoryResponse(message="No conversation memory available.", memory_size=0)
    try:
        size = pipeline.get_conversation_memory_size()
        return MemoryResponse(message="Memory size retrieved.", memory_size=size)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get memory size: {str(e)}")


@app.post("/memory/save/", response_model=MemoryResponse)
async def save_memory():
    """
    Save conversation memory to a file.
    """
    global pipeline
    if not pipeline:
        return MemoryResponse(message="No conversation memory available.", memory_size=0)
    try:
        pipeline.save_conversation_memory()
        size = pipeline.get_conversation_memory_size()
        return MemoryResponse(message="Conversation memory saved.", memory_size=size)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save memory: {str(e)}")


@app.post("/memory/load/", response_model=MemoryResponse)
async def load_memory():
    """
    Load conversation memory from a file.
    """
    global pipeline
    if not pipeline:
        return MemoryResponse(message="No conversation memory available.", memory_size=0)
    try:
        pipeline.load_conversation_memory()
        size = pipeline.get_conversation_memory_size()
        return MemoryResponse(message="Conversation memory loaded.", memory_size=size)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to load memory: {str(e)}")