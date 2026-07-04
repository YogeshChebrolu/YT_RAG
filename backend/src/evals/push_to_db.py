from core.database.supabase_client import get_supabase_client
import asyncio
import numpy as np
from evals.make_queries import make_multimodal_queries
from yt_rag.helper.get_id_from_youtube_url import get_video_id
import uuid


supabase = get_supabase_client()


def uuid_geneartor(count):
    generated_uuids=[uuid.uuid4() for i in range(count)]
    return generated_uuids

async def push_eval_to_db(video_url):
    try:
        transcript_queries, image_queries, transcripts, image_urls,image_embeddings,text_embeddings,image_query_embeddings,transcript_query_embeddings=await make_multimodal_queries(video_url)
        client=get_supabase_client()
        video_id=get_video_id(video_url)
        frame_embeddings = [emb.tolist() if isinstance(emb, np.ndarray) else emb for emb in image_embeddings]
        transcript_embeddings = [emb.tolist() if isinstance(emb, np.ndarray) else emb for emb in text_embeddings]
        image_query_embeddings = [emb.tolist() if isinstance(emb, np.ndarray) else emb for emb in image_query_embeddings]
        transcript_query_embeddings = [emb.tolist() if isinstance(emb, np.ndarray) else emb for emb in transcript_query_embeddings]
        frame_embed_ids=uuid_geneartor(len(frame_embeddings))
        transcript_ids=uuid_geneartor(len(transcript_embeddings))
        rows=[{"video_id":video_id,"image_url":image_url,"image_embedding":embeding,"query":query,"query_embedding":query_embedding,"image_id":str(image_id)} for image_url,embeding,query,query_embedding,image_id in zip(image_urls,frame_embeddings,image_queries,image_query_embeddings,frame_embed_ids)]
        client.table("imageeval").insert(rows).execute()
        
        rows=[{"video_id":video_id,"chunk":chunk,"transcript_chunk_embeddings":embeding,"query":query,"query_embedding":query_embedding,"chunk_id":str(transcript_id)} for chunk,embeding,query,query_embedding,transcript_id in zip(transcripts,transcript_embeddings,transcript_queries,transcript_query_embeddings,transcript_ids)]
        client.table("texteval").insert(rows).execute()
        print("pushed to db success")
    except Exception as e:
        print(e)
        print("pushed to db failed")

async def main():
    video_url = "https://youtu.be/MXcsW613msA?si=Tc3sgIy6R7pK5sOg"
    await push_eval_to_db(video_url)

asyncio.run(main())
