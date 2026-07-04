import os
import subprocess

from sympy import capture

def extract_frames_fast(stream_url: str, video_id:str):
    """
    Uses a single, efficient FFmpeg command to extract

    Args:
        stream_url (str)
        video_id (str)
    """
    
    output_dir = video_id
    os.makedirs(output_dir, exist_ok=True)
    print(f"Directory '{output_dir}' created. Starting FAST frame extraction...")
    
    command = [
        'ffmpeg',
        '-i', stream_url,
        '-vf', 'fps=1/60',
        f'{output_dir}/frame_%04d.jpg'
    ]
    
    try:
        subprocess.run(command, check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as e:
        print(f"Error: {e.stderr}")
        