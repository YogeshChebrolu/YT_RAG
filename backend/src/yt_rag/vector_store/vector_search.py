from yt_rag.vector_store.qdrant_db import get_qdrant_client
from qdrant_client.models import Filter, FieldCondition, MatchValue
import logging

logger = logging.getLogger(__name__)

def retrieve_frames(client, collection_name, query_embedding, top_k=5):
    frames_metadata = []
    results = client.query_points(
        collection_name=collection_name,
        query=query_embedding.tolist(),
        using="image_vector",
        query_filter=Filter(
            must=[FieldCondition(key="type", match=MatchValue(value="image"))]
        ),
        limit=top_k,
        with_payload=True
    )

    for frame in results.points:
        frames_metadata.append({
            "score": frame.score,
            "id": frame.id,
            "image_path": frame.payload.get("path"),
            "video_id": frame.payload.get("video_id")
        })

    return frames_metadata


def retrieve_transcript_chunks(client, collection_name, query_embedding, top_k=5):
    transcript_metadata = []
    results = client.query_points(
        collection_name=collection_name,
        query=query_embedding.tolist(),
        using="text_vector",
        query_filter=Filter(
            must=[FieldCondition(key="type", match=MatchValue(value="text"))]
        ),
        limit=top_k,
        with_payload=True
    )

    for chunk in results.points:
        transcript_metadata.append({
            "score": chunk.score,
            "id": chunk.id,
            "video_id": chunk.payload.get("video_id"),
            "page_content": chunk.payload.get("page_content")
        })

    return transcript_metadata


def qdrant_search(collection_name, query_embedding, top_k=5):
    client = get_qdrant_client()

    retrieved_frames_metadata = retrieve_frames(
        client=client,
        collection_name=collection_name,
        query_embedding=query_embedding,
        top_k=top_k
    )

    retrieved_transcript_metadata = retrieve_transcript_chunks(
        client=client,
        collection_name=collection_name,
        query_embedding=query_embedding,
        top_k=top_k
    )

    return retrieved_frames_metadata, retrieved_transcript_metadata
