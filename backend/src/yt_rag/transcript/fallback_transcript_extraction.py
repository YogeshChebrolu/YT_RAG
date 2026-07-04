from youtube_transcript_api import YouTubeTranscriptApi, NoTranscriptFound
from yt_rag.helper.get_id_from_youtube_url import get_video_id


def fallback_transcript_extract(youtube_url: str):
    yt_api = YouTubeTranscriptApi()
    try:
        transcript_data = yt_api.fetch(
            video_id = get_video_id(youtube_url),
            languages = ("en", 'hi', "es", "de", "te")
        )
        
        big_chunk, transcript_chunks = format_fetched_transcript(transcript_data)
        return big_chunk, transcript_chunks
    except NoTranscriptFound as e:
        return []

def format_fetched_transcript(transcript_data):
    big_chunk = ""
    transcript_chunks = []
    for snippet in transcript_data.snippets:
        big_chunk += f" {snippet.text}"
        transcript_chunks.append({
            "text": snippet.text,
            "seconds": snippet.start
        })
    
    return big_chunk, transcript_chunks
        
if __name__ == "__main__":
    big_chunk, transcript_chunks = fallback_transcript_extract("https://www.youtube.com/watch?v=GOejI6c0CMQ")
