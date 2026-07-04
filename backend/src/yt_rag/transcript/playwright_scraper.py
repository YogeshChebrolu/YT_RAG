from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
import json
import time
import asyncio

def timestamp_to_seconds(timestamp_str: str) -> int:
    time_parts = timestamp_str.split(':')
    if len(time_parts) == 3:  
        hours, minutes, seconds = map(int, time_parts)
        return hours * 3600 + minutes * 60 + seconds
    elif len(time_parts) == 2: 
        minutes, seconds = map(int, time_parts)
        return minutes * 60 + seconds
    else:  
        return int(time_parts[0])


async def ensure_english_subtitles(page):
    """
    Navigate to settings and select English subtitles if available
    """
    try:
        # Open settings
        await page.click('button.ytp-settings-button', timeout=5000)
        await page.wait_for_selector('.ytp-menuitem', timeout=5000)

        # Find the Subtitles/CC menu item
        subtitles_item = await page.query_selector('div.ytp-menuitem-label:has-text("Subtitles/CC")')
        if not subtitles_item:
            print("No subtitles/CC option found (video may not support captions).")
            return False

        # Get parent container of Subtitles/CC
        container = await subtitles_item.evaluate_handle('node => node.parentElement')

        # Get text inside .ytp-menuitem-content (current language)
        content_el = await container.query_selector('.ytp-menuitem-content')
        content_text = await content_el.inner_text() if content_el else ""

        print(f"Content Text on Subtitle item: {content_text}")

        if content_text == "English":
            print("Already English subtitles.")
            return True

        # Not English → click to open submenu
        await container.click()
        await page.wait_for_selector('.ytp-menuitem', timeout=5000)
        
        # Re-query fresh menu items to avoid previous menu items
        options = await page.query_selector_all('.ytp-menuitem')
        for i in range(len(options)):
            opt = await page.query_selector(f'.ytp-menuitem:nth-child({i+1})')
            if not opt:
                continue
            text = await opt.inner_text()
            if text == "English":
                await opt.click(force=True)
                print("Switched to English subtitles.")
                return True
            
        print(f"English subtitles not available.")
        return False
    except Exception as e:
        print(f"Error ensuring English subtitles: {e}")
        return False


async def extract_transcript(video_url: str):
    """
    Uses async playwright to automate browser navigation
    and BeautifulSoup to scrape the transcript

    Args:
        video_url (str) - url of youtube video
    """
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)  # Changed to headless for API
        page = await browser.new_page()
        
        try:
            await page.goto(video_url, wait_until="domcontentloaded", timeout=120000)

            # Step 1: Ensure English subtitles
            await ensure_english_subtitles(page)

            # Step 2: Click "Show more"
            try:
                await page.click('tp-yt-paper-button#expand', timeout=5000)
            except:
                print("No 'Show more' button found.")

            # Step 3: Click "Show transcript"
            try:
                await page.click('button:has-text("Show transcript")', timeout=5000)
            except:
                print("Transcript button not found. Maybe this video has no transcript.")
                return []

            # Step 4: Wait for transcript elements
            await page.wait_for_selector('ytd-transcript-segment-renderer', timeout=10000)

            # Step 5: Extract transcript
            html = await page.content()
            soup = BeautifulSoup(html, "html.parser")

            transcript_data = []
            for segment in soup.select("ytd-transcript-segment-renderer"):
                timestamp = segment.select_one(".segment-timestamp")
                text = segment.select_one(".segment-text")
                
                if timestamp and text:
                    timestamp_str = timestamp.get_text(strip=True)
                    
                    transcript_data.append({
                        "timestamp": timestamp_str,
                        "seconds": timestamp_to_seconds(timestamp_str),
                        "text": text.get_text(" ", strip=True)
                    })

            return transcript_data
            
        except Exception as e:
            print(f"Error extracting transcript: {e}")
            return []
        finally:
            await browser.close()


async def transcript_combined_chunk(video_url:str):
    transcript = await extract_transcript(video_url)
    big_chunk=""
    for item in transcript:
        big_chunk+=" "+item['text']
    return big_chunk , transcript




# For backward compatibility, keep a sync wrapper
def extract_transcript_sync(video_url: str):
    """
    Sync wrapper for the async extract_transcript function
    """
    import asyncio
    
    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            raise RuntimeError("Cannot call sync function from async context. Use extract_transcript directly.")
    except RuntimeError:
        pass
    
    return asyncio.run(extract_transcript(video_url))


if __name__ == '__main__':
    start_time = time.time()
    video_url = "https://youtu.be/OfOPrmnHRxw?si=PZcOEUnRMrwcfOuS"
    
    transcript = asyncio.run(transcript_combined_chunk(video_url))
    
    end_time = time.time()
    print(f"Transcript extracted in {end_time-start_time:.2f} seconds")
    print(transcript)

"""     with open("transcript1.json", "w", encoding="utf-8") as f:
        json.dump(transcript, f, ensure_ascii=False, indent=2) """
