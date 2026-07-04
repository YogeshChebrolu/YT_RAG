from yt_rag.vector_store.pg_vector_helpers import match_transcript_chunks,match_frame_urls,upsert_frames,video_info,upsert_transcript_chunks_embeddngs_to_collection,upsert_image_embeddings_to_collection,video_exists,push_to_bucket,upsert_transcript

class PG_Vector:
  def __init__(self,video_id):
    self.video_id=video_id
    self.urls=None
    self.generated_uuids_frames=None
    self.generated_uuids_transcript=None

  def does_video_exist(self,video_id):
    resonse=video_exists(video_id=video_id)
    if resonse:
      print(f"video exists with id {video_id}")
      return True
    else:
      print(f"Video doesn't exist with video id {video_id}")
      return False
      
  def video_info(self,summary,processed="SUCCESS"):
    response=video_info(self.video_id,summary,table_name="videos",processed=processed)

  def push_to_bucket(self,image_folder):
    self.urls=push_to_bucket(image_folder=image_folder)
    return self.urls
  
  def upsert_frames(self):
    self.generated_uuids_frames=upsert_frames(video_id=self.video_id,image_urls=self.urls,table_name="frames")
    return self.generated_uuids_frames
  
  def upsert_frame_embeddings(self,embeddings):
   response= upsert_image_embeddings_to_collection(video_id=self.video_id,frame_embeddings=embeddings,frame_embed_ids=self.generated_uuids_frames,table_name="frame_embeddings")
   return response
  
  def upsert_transcript(self,transcipts):
    self.generated_uuids_transcript=upsert_transcript(video_id=self.video_id,transcripts=transcipts)
    return self.generated_uuids_transcript
  def upsert_transcript_embeddings(self,transcript_embeddings):
    response=upsert_transcript_chunks_embeddngs_to_collection(video_id=self.video_id,transcript_embeddings=transcript_embeddings,transcript_ids=self.generated_uuids_transcript)
    return response

class PG_Vector_search:
  def __init__(self):
    pass
  def match_transcript(self,video_id,query_embedding):
    transcript_data=match_transcript_chunks(video_id,query_embedding)
    return transcript_data
  def match_frames(self,video_id,query_embedding):
    frames_data= match_frame_urls(video_id=video_id,query_embedding=query_embedding)
    return frames_data