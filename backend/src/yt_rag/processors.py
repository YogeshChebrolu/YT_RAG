import asyncio
import logging
import json
from typing import List, Dict
import traceback
from yt_rag.transcript.chunking import get_transcript_chunks
from yt_rag.frames.collect_frames import collect_frames_from_ffmpeg
from yt_rag.vector_store.embeddings import create_embeddings_from_folder, create_text_embeddings_batch
from yt_rag.helper.get_id_from_youtube_url import get_video_id
from yt_rag.vector_store.pg_vector_operations import PG_Vector
from yt_rag.llm_service.summarize_transcript import summarize_transcript
DEFAULT_CHUNK_DURATION = 50
DEFAULT_OVERLAP_ENTRIES = 5

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def extract_video_content(youtube_url: str):
    transcript_chunks = None
    image_folder_path = None
    big_chunk = None
    
    try:
        logger.info(f"Starting content extraction for video: {youtube_url}")
        
        try:
            logger.info("Starting transcript extraction...")
            transcript_chunks, big_chunk = await get_transcript_chunks(
                youtube_url=youtube_url,
                chunk_duration=DEFAULT_CHUNK_DURATION,
                overlap_entires=DEFAULT_OVERLAP_ENTRIES
            )
            logger.info(f"Transcript extraction completed: {len(transcript_chunks) if transcript_chunks else 0} chunks")
        except Exception as e:
            logger.error(f"Transcript extraction failed: {e}")
            logger.error(f"Transcript traceback: {traceback.format_exc()}")
        
        try:
            logger.info("Starting frames extraction...")
            image_folder_path = await asyncio.to_thread(
                collect_frames_from_ffmpeg,
                youtube_url=youtube_url
            )
            logger.info(f"Frames extraction completed")
        except Exception as e:
            logger.error(f"Frames extraction failed: {e}")
            logger.error(f"Frames traceback: {traceback.format_exc()}")
        
        logger.info(f"Content extraction summary - Transcript chunks: {len(transcript_chunks) if transcript_chunks else 0}")
        
        return transcript_chunks, image_folder_path, big_chunk
    
    except Exception as e:
        logger.error(f"Unexpected error in extract_video_content for {youtube_url}: {e}")
        logger.error(f"Full traceback: {traceback.format_exc()}")
        return transcript_chunks, image_folder_path, big_chunk

async def process_image_embeddings(pg_vector: PG_Vector, image_folder_path: str) -> bool:
    """
    Process and store image embeddings in the PGVector database.
    """
    try:
        image_urls = pg_vector.push_to_bucket(image_folder_path)
        if not image_urls:
            logger.error("Failed to push images to bucket")
            return False
        
        frame_uuids = pg_vector.upsert_frames()
        if not frame_uuids:
            logger.error("Failed to upsert frames")
            return False
        
        image_embeddings = create_embeddings_from_folder(image_folder_path)
        if not image_embeddings:
            logger.error("No image embeddings generated")
            return False
            
        success = pg_vector.upsert_frame_embeddings(image_embeddings)
        if not success:
            logger.error("Failed to upsert image embeddings")
            return False
            
        logger.info(f"Successfully processed and stored {len(image_urls)} image embeddings")
        return True
        
    except Exception as e:
        logger.error(f"Error processing image embeddings: {e}")
        logger.error(f"Full traceback: {traceback.format_exc()}")
        return False

async def process_text_embeddings(pg_vector: PG_Vector, transcript_chunks: List[Dict]) -> bool:
    """
    Process and store text embeddings from transcript chunks in the PGVector database.
    """
    try:
        texts_to_embed = [chunk["page_content"] for chunk in transcript_chunks]

        text_embeddings = create_text_embeddings_batch(texts_to_embed)
        if not text_embeddings:
            logger.error("No text embeddings generated")
            return False
            
        transcript_uuids = pg_vector.upsert_transcript(transcript_chunks)
        if not transcript_uuids:
            logger.error("Failed to upsert transcript chunks")
            return False
            
        success = pg_vector.upsert_transcript_embeddings(text_embeddings)
        if not success:
            logger.error("Failed to upsert transcript embeddings")
            return False
            
        logger.info(f"Successfully processed and stored {len(transcript_chunks)} text embeddings")
        return True
        
    except Exception as e:
        logger.error(f"Error processing text embeddings: {e}")
        logger.error(f"Full traceback: {traceback.format_exc()}")
        return False

async def process_youtube_video(youtube_url: str):

    try:
        video_id = get_video_id(youtube_url)
        pg_vector = PG_Vector(video_id)
        
        if pg_vector.does_video_exist(video_id):
            logger.info(f"Video {video_id} already exists in database, skipping processing")
            return video_id
        else:
            pg_vector.video_info(summary="",processed="PROCESSING")
        transcript_chunks, image_folder_path, big_chunk = await extract_video_content(youtube_url)
        
        if transcript_chunks:
            with open(f"transcript_{video_id}.json", "w", encoding="utf-8") as f:
                data = json.dumps(transcript_chunks, default=str)
                f.write(data)
        
        if image_folder_path:
            success = await process_image_embeddings(pg_vector, image_folder_path)
            if not success:
                logger.warning("Image processing failed")
        else:
            logger.warning("No image frames extracted, skipping image processing")
        
        if transcript_chunks:
            success = await process_text_embeddings(pg_vector, transcript_chunks)
            if not success:
                logger.warning("Text processing failed")
        else:
            logger.warning("No transcript chunks extracted, skipping text processing")
        
        if big_chunk:
            summary = summarize_transcript(big_chunk)
            pg_vector.video_info(summary)
            
        return video_id
        
    except Exception as e:
        logger.error(f"Error in video processing pipeline: {e}")
        logger.error(f"Full traceback: {traceback.format_exc()}")
        return False

async def main():
    youtube_url = "https://www.youtube.com/watch?v=__yqhaqRfqw"
    
    logger.info("Starting YouTube RAG processing pipeline")
    success = await process_youtube_video(youtube_url)
    
    if success:
        logger.info("Video processing completed successfully!")
    else:
        logger.error("Video processing failed!")
        return 1
    
    return 0

if __name__ == "__main__":
    asyncio.run(main())