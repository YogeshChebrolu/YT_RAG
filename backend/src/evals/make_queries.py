from yt_rag.llm_service.gemini_client import get_gemini_client
from yt_rag.processors import extract_video_content
import asyncio
from yt_rag.vector_store.pg_vector_operations import PG_Vector
from google.genai import types
from yt_rag.helper.get_id_from_youtube_url import get_video_id
import aiohttp
from yt_rag.vector_store.embeddings import create_embeddings_from_folder,create_text_embeddings_batch
prompt="I am working on a project to evaluate the performance of a multimodal retrieval system. I have a video and I want to generate queries for the video. Please generate a query for the following transcript: {transcript}."
image_prompt="I am working on a project to evaluate the performance of a multimodal retrieval system. I have a frame of a video and I want to generate queries for the frame. Please generate a query for the following image, note you should generate exactly one most relevent query and no other text"

async def make_multimodal_queries(video_url: str):
    loop = asyncio.get_running_loop()
    transcript_chunks, image_folder_path, big_chunk = await  extract_video_content(video_url)
    
    llm_client = get_gemini_client()
    
    transcript_queries = []
    transcripts = []
    image_queries = []
    
    video_id = get_video_id(video_url)
    pg_vector = PG_Vector(video_id)
    
    image_urls = await loop.run_in_executor(
        None, lambda: pg_vector.push_to_bucket(image_folder_path)
    )
    
    async def process_image(image_url: str):
        async with aiohttp.ClientSession() as session:
            async with session.get(image_url) as response:
                if response.status != 200:
                    return ""
                image_bytes = await response.read()
                image = types.Part.from_bytes(
                    data=image_bytes, mime_type="image/jpeg"
                )
                response = await loop.run_in_executor(
                    None,
                    lambda: llm_client.models.generate_content(
                        model="gemini-2.0-flash",
                        contents=[image],
                        config={
                            "system_instruction": image_prompt,
                            "temperature": 0.5,
                        },
                    )
                )
                return response.text
    
    async def process_transcript(transcript: str):
        response = await loop.run_in_executor(
            None,
            lambda: llm_client.models.generate_content(
                model="gemini-2.0-flash",
                contents="please generate a query for the transcript, remember i just need only one most relevant query, i don't need any other text",
                config={
                    "system_instruction": prompt.format(transcript=transcript),
                    "temperature": 0.5,
                },
            )
        )
        return response.text

    image_tasks = [process_image(image_url) for image_url in image_urls]
    transcript_tasks = [
        process_transcript(transcript["page_content"])
        for transcript in transcript_chunks]
    image_embeddings = create_embeddings_from_folder(image_folder_path)
    texts_to_embed=[transcript["page_content"] for transcript in transcript_chunks]
    text_embeddings = create_text_embeddings_batch(texts_to_embed)
    image_queries = await asyncio.gather(*image_tasks, return_exceptions=True)
    transcript_queries = await asyncio.gather(*transcript_tasks, return_exceptions=True)
    transcript_query_embeddings=create_text_embeddings_batch(transcript_queries)
    image_query_embeddings=create_text_embeddings_batch(image_queries)
    
    transcripts = [transcript["page_content"] for transcript in transcript_chunks]
    
    return transcript_queries, image_queries, transcripts, image_urls,image_embeddings,text_embeddings,image_query_embeddings,transcript_query_embeddings
  

