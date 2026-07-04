import asyncio
import re
import json
import uuid
import logging
from yt_rag.transcript.fallback_transcript_extraction import fallback_transcript_extract
from yt_rag.transcript.playwright_scraper import extract_transcript , transcript_combined_chunk
from yt_rag.helper.get_id_from_youtube_url import get_video_id
logger = logging.getLogger(__name__)


def trascript_chunking_by_time(
    transcripts,
    video_id: str,
    chunk_duration=150,
    overlap_entires=5
):
    try:
        if not transcripts:
            raise ValueError("Transcript is not available")
    
        chunks = []
        current_chunk = []
        current_start = 0

        for entry in transcripts:
            start_time = entry["seconds"]
            if not current_chunk:
                current_start = start_time
            
            if start_time - current_start < chunk_duration:
                current_chunk.append(entry)
            else:
                chunk_text = " ".join(e["text"] for e in current_chunk)
                chunks.append({
                    "page_content":chunk_text,
                    "metadata":{"start":current_start, "video_id": video_id},
                    "id": str(uuid.uuid4())
                })

                current_chunk = current_chunk[-overlap_entires:]
                current_start = current_chunk[0]["seconds"]
                current_chunk.append(entry)
                
        if current_chunk:
            chunk_text = " ".join(e["text"] for e in current_chunk)
            chunks.append({
                "page_content":chunk_text,
                "start_time":current_start
            })
    
        return chunks

    except Exception as e:
        logger.error(f"Error chunking transcript: {str(e)}")
        return None

async def get_transcript_chunks(youtube_url: str, chunk_duration: int, overlap_entires):
    
    try:
        big_chunk,transcript_data = await transcript_combined_chunk(youtube_url)
    except Exception as e:
        logger.error(f"Playwright extraction failed with error: {str(e)}")
        transcript_data = []    
    
    if transcript_data:
        logger.info("Transcript data extracted with playwright")
        
        video_id = get_video_id(youtube_url)
        transcript_chunks = trascript_chunking_by_time(
            transcript_data,
            video_id,
            chunk_duration=chunk_duration,
            overlap_entires=overlap_entires        
        )
        logger.info(f"Successfully chunked into : {len(transcript_chunks)} chunks")
        return transcript_chunks , big_chunk
    else:
        print(f"Using fall back to extract transcript")
        big_chunk, fallback_transcript_data = fallback_transcript_extract(youtube_url)
        if fallback_transcript_data:
            logger.info("Transcript data extracted with fallback YoutubeTranscriptAPI")
        
            video_id = get_video_id(youtube_url)
            transcript_chunks = trascript_chunking_by_time(
                fallback_transcript_data,
                video_id,
                chunk_duration=200,
                overlap_entires=5        
            )
            logger.info(f"Successfully chunked into : {len(transcript_chunks)} chunks")
            return big_chunk, transcript_chunks
        else:
            return []

if __name__ == "__main__":
    big_chunk, transcript_chunks = asyncio.run(get_transcript_chunks("https://www.youtube.com/watch?v=GOejI6c0CMQ", 200, 5))
    # print(big_chunk, transcript_chunks)
    # print(len(transcript_chunks))
    