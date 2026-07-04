from yt_rag.transcript.chunking import get_transcript_chunks
from core.database.supabase_client import get_supabase_client
import asyncio
import pandas as pd
import os
import asyncio
from datetime import datetime
from typing import List

BATCH_SIZE  = 1000     # process 1000 URLs at a time
CONCURRENCY = 15       # keep small on slow networks
TIMEOUT_S   = 750       # per-URL timeout
PAUSE_BETWEEN_BATCHES_S = 5
filtered_data=pd.read_csv("src/evals/filtered_data.csv")
urls=[url for url in filtered_data['video_url']]
_supabase=get_supabase_client()

async def extract_videos_content(url):
    transcript_chunks, big_chunk = await get_transcript_chunks(
        youtube_url=url,
        chunk_duration=50,
        overlap_entires=5
    )
    print(big_chunk)
    return transcript_chunks, big_chunk


def push_transcript_chunk(url: str, transcript: str) -> bool:
    try:
        if not transcript or transcript.strip() == "":
            print(f"Empty transcript for {url}, skipping push")
            return False
            
        row = {"url": url, "big_chunk": transcript, "summary": " "}
        _supabase.table("transcripts_for_summary") \
            .insert(row) \
            .execute()
        print(f"✓ Pushed transcript for {url[:50]}...")
        return True
    except Exception as e:
        print(f"✗ DB push failed for {url[:50]}...: {e}")
        return False
"""
async def _process_one(url: str, sem: asyncio.Semaphore) -> str:
    try:
        async with sem:
            chunks, big = await asyncio.wait_for(extract_videos_content(url), timeout=TIMEOUT_S)
        ok = push_transcript_chunk(url, big or "")
        return "ok" if ok else "failed"
    except asyncio.TimeoutError:
        print(f"⏱ Timeout for {url[:50]}...")
        return "failed"
    except Exception as e:
        print(f"✗ Error processing {url[:50]}...: {e}")
        return "failed"""
async def _process_one(url: str, sem: asyncio.Semaphore) -> str:
    try:
        async with sem:
            chunks, big = await asyncio.wait_for(extract_videos_content(url), timeout=TIMEOUT_S)
        
        # Log extraction success
        if big and big.strip():
            print(f"✓ Transcript extracted ({len(big)} chars) for {url[:50]}...")
        else:
            print(f"⚠ Empty transcript for {url[:50]}...")
            return "failed"
            
        ok = push_transcript_chunk(url, big)
        return "ok" if ok else "failed"
        
    except asyncio.TimeoutError:
        print(f"⏱ Timeout for {url[:50]}...")
        return "failed"
    except Exception as e:
        print(f"✗ Error processing {url[:50]}...: {e}")
        return "failed"
def chunked(lst: List[str], n: int):
    for i in range(0, len(lst), n):
        yield lst[i:i+n]

async def run_urls(urls: List[str]):
    sem = asyncio.Semaphore(CONCURRENCY)
    batch_num = 0
    total = len(urls)
    print(f"Starting: {total} URLs | BATCH_SIZE={BATCH_SIZE} | CONCURRENCY={CONCURRENCY}")

    for batch_urls in chunked(urls, BATCH_SIZE):
        batch_num += 1
        print(f"\n[Batch {batch_num}] size={len(batch_urls)}")

        tasks = [asyncio.create_task(_process_one(u, sem)) for u in batch_urls]
        results = await asyncio.gather(*tasks)

        ok = results.count("ok")
        failed = results.count("failed")
        print(f"[Batch {batch_num} finished] ok={ok} failed={failed}")

        await asyncio.sleep(PAUSE_BETWEEN_BATCHES_S)

    print("\nAll batches done ")

if __name__ == "__main__":
    asyncio.run(run_urls(urls))

