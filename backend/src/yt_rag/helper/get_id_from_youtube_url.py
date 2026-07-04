import re

def get_video_id(youtube_url: str) -> str:
    YT_ID_RE = re.compile(r'(?:v=|youtu\.be/|embed/|shorts/)([A-Za-z0-9_-]{11})')
    m = YT_ID_RE.search(youtube_url)
    return m.group(1) if m else None
