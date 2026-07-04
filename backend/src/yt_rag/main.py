from yt_rag.llm_service.gemini_with_memory import ChatGemini, clear_memory, get_memory_size, save_memory_to_file, load_memory_from_file
from yt_rag.processors import process_youtube_video
from yt_rag.vector_store.vector_search import qdrant_search
from yt_rag.vector_store.embeddings import create_text_embeddings
from yt_rag.llm_service.cleaningextracted_data import extractchunk, extractimagename, image2bytes_converter
from yt_rag.llm_service.system_prompt import system_prompt


"""
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
            pg_vector.video_info(big_chunk)
            
        return video_id
        
    except Exception as e:
        logger.error(f"Error in video processing pipeline: {e}")
        logger.error(f"Full traceback: {traceback.format_exc()}")
        return False

async def main():
    youtube_url = "https://youtu.be/wCNIhFdhgLE?si=A0isI2yoAwtsFV9C"
    
    logger.info("Starting YouTube RAG processing pipeline")
    success = await process_youtube_video(youtube_url)
    
    if success:
        logger.info("Video processing completed successfully!")
    else:
        logger.error("Video processing failed!")
        return 1
    
    return 0
"""

class RAGPipeline:
    def __init__(self, video_url, memory_file="conversation_memory.json"):
        self.video_url = video_url
        self.video_id = None
        self.memory_file = memory_file
        self.conversation_memory = []

    async def process_video(self):
        """Process the YouTube video and extract its ID."""
        self.video_id = await process_youtube_video(self.video_url)
        if self.video_id:
            self.memory_file = f"conversation_memory_{self.video_id}.json"
        self.load_conversation_memory()
        return self.video_id

    def query_video(self, query, collection_name=None, embeddings=None):
        """Query the video content and retrieve relevant frames and transcript chunks."""
        embeddings_in_sameclass = create_text_embeddings(query)
        effective_collection_name = collection_name if collection_name else self.video_id
        effective_embeddings = embeddings if embeddings else embeddings_in_sameclass
        retrieved_frames_metadata, retrieved_transcript_metadata = qdrant_search(
            collection_name=effective_collection_name, 
            query_embedding=effective_embeddings
        )
        image_paths = extractimagename(retrieved_frames_metadata)
        chunks = extractchunk(retrieved_transcript_metadata)
        image_bytes = image2bytes_converter(image_paths)
        return image_bytes, chunks

    def query_gemini(self, query, collection_name=None, embeddings=None):
        """Query Gemini with video context and conversation memory."""
        image_bytes, chunks = self.query_video(query, collection_name, embeddings)
        retrieval_chunk = ""
        for conv in chunks:
            retrieval_chunk += conv
            retrieval_chunk += "\n"
        response = ChatGemini(
            prompt=query,
            system_prompt=system_prompt,
            images=image_bytes,
            use_memory=True,
            conversation_memory=self.conversation_memory
        )
        return response.text

    def chatgemini(self, prompt):
        """Chat with Gemini using conversation memory."""
        response = ChatGemini(
            prompt=prompt,
            system_prompt=system_prompt,
            images=None,
            use_memory=True,
            conversation_memory=self.conversation_memory
        )
        return response.text

    def clear_conversation_memory(self):
        """Clear the conversation memory."""
        clear_memory(self.conversation_memory)

    def get_conversation_memory_size(self):
        """Get the current number of messages in conversation memory."""
        return get_memory_size(self.conversation_memory)

    def save_conversation_memory(self):
        """Save the conversation memory to a JSON file."""
        save_memory_to_file(self.memory_file, self.conversation_memory)

    def load_conversation_memory(self):
        """Load conversation memory from a JSON file."""
        load_memory_from_file(self.memory_file, self.conversation_memory)