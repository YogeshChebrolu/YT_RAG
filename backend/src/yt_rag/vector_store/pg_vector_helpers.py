import logging
import uuid
from core.database.supabase_client import get_supabase_client
from core.database.db_helpers import list_folder_contents_os_walk
import mimetypes
import numpy as np
logger = logging.getLogger(__name__)
client=get_supabase_client()


def upsert_image_embeddings_to_collection(video_id:str,frame_embeddings,frame_embed_ids,table_name="frame_embeddings"):
  try:
    print("Entering upsert_embeddings_images_to_collection")
    frame_embeddings = [emb.tolist() if isinstance(emb, np.ndarray) else emb for emb in frame_embeddings]
    rows=[{"video_id":video_id,"frame_embed_id":frame_embed_id,"vector_rep":embeding} for frame_embed_id,embeding in zip(frame_embed_ids,frame_embeddings)]
    client.table(table_name).insert(rows).execute()
    print("Completed image_embeddings_collection_upsert")
    return True
  except Exception as e:
    print(e)
    return False

def upsert_transcript_chunks_embeddngs_to_collection(video_id:str,transcript_embeddings,transcript_ids,table_name="transcript_chunk_embeddings"):
  try:
    print("Entering upsert_transcript_chunks_to_collection")
    transcript_embeddings = [emb.tolist() if isinstance(emb, np.ndarray) else emb for emb in transcript_embeddings]
    rows=[{"video_id":video_id,"transcript_embed_id":frame_embed_id,"vector_rep":embeding} for frame_embed_id,embeding in zip(transcript_ids,transcript_embeddings)]
    client.table(table_name).insert(rows).execute()
    print("Completed upsert_transcript_chunks_to_collection")
    return True
  except Exception as e:
    print(e)
    return False

def push_to_bucket(image_folder,supabase_url:str="https://sofowbahdzuboflvuprw.supabase.co",bucket_name="images"):
  files=list_folder_contents_os_walk(image_folder)
  try :
    for file in files:
        ctype, _ = mimetypes.guess_type(file)
        ctype = ctype or "application/octet-stream"
        with open(file, "rb") as f:
            client.storage.from_(bucket_name).upload(
                path=file,
                file=f,
                file_options={"content-type": ctype, "cache-control": "3600", "upsert": "true"},
            )
    image_urls=[]
    for image_file in files:
        url=f"{supabase_url}/storage/v1/object/public/{bucket_name}/{image_file}"
        image_urls.append(url)
    return image_urls
  except Exception as e:
    print(e)
    return False

def video_info(video_id,summary,table_name="videos",processed="SUCCESS"):
  try:
    print("Video info filling")
    rows=[{"video_id":video_id,"summary":summary,"processed":processed}]
    client.table(table_name).upsert(rows).execute()
    print("video info filling completed")
    return True
  except Exception as e:
     print(e)
     return False

def uuid_geneartor(count):
    generated_uuids=[uuid.uuid4() for i in range(count)]
    return generated_uuids


def upsert_frames(video_id,image_urls,table_name="frames"):
  count=len(image_urls)
  generated_uuids=uuid_geneartor(count)
  try:
    print("Entering upsert_frames")
    rows=[{"video_id":video_id,"frame_url":frame_url,"id":str(frame_id)} for frame_url,frame_id in zip(image_urls,generated_uuids)]
    client.table(table_name).insert(rows).execute()
    print("Completed upsert_frames")
    return [str(frame_id) for frame_id in  generated_uuids]
  except Exception as e:
    print(e)
    return False


def upsert_transcript(video_id,transcripts,table_name="transcript_chunks"):
  count=len(transcripts)
  generated_uuids=uuid_geneartor(count)
  try:
    print("Entering upsert_transcript")
    rows=[{"video_id":video_id,"content":transcript,"id":str(transcript_id)} for transcript,transcript_id in zip(transcripts,generated_uuids)]
    client.table(table_name).insert(rows).execute()
    print("Completed upsert_transcript")
    return [str(transcript_id) for transcript_id in  generated_uuids]
  except Exception as e:
    print(e)
    return False
  

def match_frame_urls(video_id,query_embedding,match_count=3):
  try:
    print("matching frames to url")
    query_embedding=query_embedding.tolist() if isinstance(query_embedding, np.ndarray) else query_embedding

    response=client.rpc(
      "match_frame_urls",
      {
        "in_video_id":video_id,
        "query_embedding":query_embedding,
        "match_count":match_count
      }
    ).execute()
    return response.data
  except Exception as e:
    print(e)
    return False
  
def match_transcript_chunks(in_video_id: str,query_embedding,match_count: int = 3,):
    try:
      query_embedding=query_embedding.tolist() if isinstance(query_embedding, np.ndarray) else query_embedding
      print("Matching transcript to chunks")
      res = client.rpc(
        "match_transcript_chunks",
        {
          "in_video_id": in_video_id,
          "query_embedding": query_embedding,
          "match_count": match_count,
      }).execute()
      print("Matching transcript to chunks completed")
      return res.data
    except Exception as e:
      print(e)
      return False
    
def video_exists(video_id: str) -> bool:
    supabase = get_supabase_client()
    response = (
        supabase.table("videos")
        .select("video_id")
        .eq("video_id", video_id)
        .limit(1)
        .execute()
    )
    return len(response.data) > 0
