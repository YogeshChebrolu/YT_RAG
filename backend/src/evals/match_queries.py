from core.database.supabase_client import get_supabase_client
from yt_rag.vector_store.embeddings import create_text_embeddings
import numpy as np
supabase = get_supabase_client()
def match_text_queries(query: str, video_id: str):
  try:
    query_embedding = create_text_embeddings(query)
    query_embedding = query_embedding.tolist() if isinstance(query_embedding, np.ndarray) else query_embedding
    response = supabase.rpc("match_text_evals", {
      "in_video_id": video_id,
      "query_embedding": query_embedding
    }).execute()
    return response.data
  except Exception as e:
    print(e)
    return False

def match_image_queries(query: str, video_id: str):
  try:
    query_embedding = create_text_embeddings(query)
    query_embedding = query_embedding.tolist() if isinstance(query_embedding, np.ndarray) else query_embedding
    response = supabase.rpc("match_image_evals", {
      "in_video_id": video_id,
      "query_embedding": query_embedding
    }).execute()
    return response.data
  except Exception as e:
    print(e)
    return False

supabase = get_supabase_client()

def fetch_texteval_rows(video_id: str):
    response = supabase.table("texteval").select("*").eq("video_id", video_id).execute()
    return response.data if response.data else []

def fetch_imageeval_rows(video_id: str):
    response = supabase.table("imageeval").select("*").eq("video_id", video_id).execute()
    return response.data if response.data else []

def compute_rank(results, target_id, id_field):
    for rank, result in enumerate(results, start=1):
        if result[id_field] == target_id:
            return rank
    return float('inf')  

def evaluate_retrieval(video_id: str, modality: str = 'text', k_values=[1, 3, 5]):
    if modality == 'text':
        rows = fetch_texteval_rows(video_id)
        match_func = match_text_queries
        id_field = 'chunk_id'
        content_field = 'chunk'
    elif modality == 'image':
        rows = fetch_imageeval_rows(video_id)
        match_func = match_image_queries
        id_field = 'image_id'
        content_field = 'image_url'
    else:
        raise ValueError("Modality must be 'text' or 'image'")

    if not rows:
        print(f"No data for video_id {video_id} in {modality} table.")
        return

    ranks = []
    similarities = []
    total_queries = len(rows)

    for row in rows:
        query = row['query']
        target_id = row[id_field]
        
        results = match_func(query, video_id)  
        
        rank = compute_rank(results, target_id, id_field)
        ranks.append(rank)
        
        gt_result = next((r for r in results if r[id_field] == target_id), None)
        if gt_result:
            similarities.append(gt_result['similarity'])

    mean_rank = np.mean([r for r in ranks if r != float('inf')]) if ranks else 0
    mrr = np.mean([1/r if r != float('inf') else 0 for r in ranks])
    avg_similarity = np.mean(similarities) if similarities else 0

    hit_rates = {}
    for k in k_values:
        hits = sum(1 for r in ranks if r <= k)
        hit_rates[k] = (hits / total_queries) * 100

    print(f"Evaluation for {modality} modality on video_id {video_id}:")
    print(f"Total Queries: {total_queries}")
    print(f"Mean Rank: {mean_rank:.2f}")
    print(f"MRR: {mrr:.4f}")
    print(f"Average Similarity: {avg_similarity:.4f}")
    for k, rate in hit_rates.items():
        print(f"Hit Rate @ {k}: {rate:.2f}%")
    return {
        "mrr": mrr,
        "mean_rank": mean_rank,
        "avg_similarity": avg_similarity,
        "hit_rates": hit_rates,
        "total_queries": total_queries
    }

if __name__ == "__main__":
    video_id = "MXcsW613msA"
    evaluate_retrieval(video_id, modality='text')
    evaluate_retrieval(video_id, modality='image')