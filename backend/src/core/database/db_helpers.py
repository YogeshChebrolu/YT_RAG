from core.database.supabase_client import get_supabase_client
import os

def video_exists(video_id: str) -> bool:
    supabase = get_supabase_client()
    response = (
        supabase.table("videos")
        .select("id")
        .eq("video_id", video_id)
        .limit(1)
        .execute()
    )
    return len(response.data) > 0


def push_video_details(id,video_id,summary_text):
  """
  video_id text primary key not null,
  created_at timestamp with time zone not null default now(),
  title text,
  summary text,
  channel_name text,
  processed public.video_status
  """
  supabase=get_supabase_client()
  response = (
    supabase.table("videos")
    .insert({"video_id": video_id,"summary":summary_text})
    .execute()
  )
  return response


def list_folder_contents_os_walk(start_path):
    total_files=[]
    for root, dirs, files in os.walk(start_path):
        if dirs:
          for dir in dirs:
            for file in files:
              file_path=root+"/"+dir+"/"+file
              total_files.append(file_path)
        else:
          for file in files:
            file_path=root+"/"+file
            total_files.append(file_path)
           
    return total_files


def match_notes_headings(user_id,query_embedding):
    try:
      query_embedding=query_embedding.tolist() if isinstance(query_embedding, np.ndarray) else query_embedding
      print("Matching notes with headings")
      res = client.rpc(
        "match_notes_headings",
        {
          "user_id": user_id,
          "query_embedding": query_embedding
          }).execute()
      print("Matching notes with headings complete")
      return res.data
    except Exception as e:
      print(e)
      return False