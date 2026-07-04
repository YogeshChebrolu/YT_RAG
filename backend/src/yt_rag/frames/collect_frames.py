import re
import uuid
import yt_dlp
from yt_rag.frames.ffmpeg_frame_extraction import extract_frames_fast
from yt_rag.helper.get_id_from_youtube_url import get_video_id
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

def list_images(dir_path: str):
    path = Path(dir_path)
    exts = ("*.jpg", "*.jpeg", "*.png", "*.webp")
    files = [f.resolve() for pattern in exts for f in path.glob(pattern)]
    return sorted(files)


def get_video_info(youtube_url: str) -> dict:
    ydl_opts = {'format': 'best[ext=mp4]'}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(
            url=youtube_url,
            download=False
        )
        stream_url = info.get("url", "")
        duration = int(info.get("duration", ""))
        print(f"Successfully found stream URL for a video of {duration} seconds.")
        return {
            "stream_url": stream_url,
            "duration": duration
        }



def collect_frames_from_ffmpeg(youtube_url: str):
    video_id = get_video_id(youtube_url)
    logger.info(f"Starting frame extraction for video ID: {video_id}")
    
    video_info = get_video_info(youtube_url)
    if not video_info or "stream_url" not in video_info:
        logger.error(f"Could not retrieve video info for {youtube_url}. Aborting.")
        return
    
    stream_url = video_info.get("stream_url", "")
    logger.info("Successfully retrieved video stream URL")
    
    extract_frames_fast(
        stream_url= stream_url,
        video_id=video_id
    )
    logger.info("Frames extraction completed")
    
    images_folder_path = f"./{video_id}"
    
    return images_folder_path